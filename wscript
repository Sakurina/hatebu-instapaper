import TaskGen
import Utils
import os
import glob

top = '.'
out = 'build'

TaskGen.declare_chain(
    name='objc',
    rule='${C_COMPILER} -c ${GLOBAL_CFLAGS} ${SRC} -o ${TGT}',
    ext_in='.m',
    ext_out='.o',
    reentrant=False
)

TaskGen.declare_chain(
    name='objcpp',
    rule='${CPP_COMPILER} -c ${GLOBAL_CFLAGS} ${SRC} -o ${TGT}',
    ext_in='.mm',
    ext_out='.o',
    reentrant=False
)

def configure(conf):
  print('→ configuring global settings')
  # user-level stuff
  conf.env.CPP_COMPILER_EXEC = 'arm-apple-darwin10-llvm-g++-4.2'
  conf.env.C_COMPILER_EXEC = 'arm-apple-darwin10-llvm-gcc-4.2'
  conf.env.SDK_VERSION = '5.0'
  conf.env.MIN_OS_VERSION = '30000'
  # deb package
  conf.env.PREFIX = os.getcwd()+'/net.r-ch.hatebu-instapaper'
  # nitty-gritty
  conf.env.PLATFORM = '/Developer/Platforms/iPhoneOS.platform'
  conf.env.PLATFORM_BIN = conf.env.PLATFORM+'/Developer/usr/bin'
  conf.env.CPP_COMPILER = conf.env.PLATFORM_BIN+'/'+conf.env.CPP_COMPILER_EXEC
  conf.env.C_COMPILER = conf.env.PLATFORM_BIN+'/'+conf.env.C_COMPILER_EXEC
  conf.env.SDK = conf.env.PLATFORM+'/Developer/SDKs/iPhoneOS'+conf.env.SDK_VERSION+'.sdk'
  #  relative paths
  conf.env.FRAMEWORKS_DIR = conf.env.SDK+"/System/Library/Frameworks"
  conf.env.PRV_FRAMEWORKS_DIR = conf.env.SDK+"/System/Library/PrivateFrameworks"
  conf.env.LIB_DIR = conf.env.SDK+"/usr/lib"
  conf.env.SYSTEM_LIB_DIR = conf.env.SDK+"/usr/lib/system"
  conf.env.LOCAL_LIB_DIR = "/Users/sakurina/src/_jbenv/lib"
  conf.env.SDK_INCLUDE_DIR = conf.env.SDK+"/usr/include"
  conf.env.PLAT_INCLUDE_DIR = conf.env.PLATFORM+"/Developer/usr/include"
  conf.env.SIM_INCLUDE_DIR = "/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator"+conf.env.SDK_VERSION+".sdk/usr/include"
  #  default compile flags
  conf.env.GLOBAL_CFLAGS = "-I"+conf.env.SDK_INCLUDE_DIR+" -I"+conf.env.PLAT_INCLUDE_DIR+" -I"+conf.env.SIM_INCLUDE_DIR+" -F"+conf.env.FRAMEWORKS_DIR+" -F"+conf.env.PRV_FRAMEWORKS_DIR+" -D__IPHONE_OS_VERSION_MIN_REQUIRED="+conf.env.MIN_OS_VERSION+" -Os"
  #  default linker flags
  conf.env.GLOBAL_LDFLAGS = "-F"+conf.env.FRAMEWORKS_DIR+" -F"+conf.env.PRV_FRAMEWORKS_DIR+" -L"+conf.env.LIB_DIR+" -L"+conf.env.SYSTEM_LIB_DIR+" -L"+conf.env.LOCAL_LIB_DIR+" -lobjc -ObjC++ -framework CoreFoundation -framework Foundation"
  conf.env.SUBSTRATE_LDFLAGS = conf.env.GLOBAL_LDFLAGS+" -dynamiclib -lsubstrate"
  # recurse into subprojects
  conf.recurse('dylib')
  pass

def build(bld):
  print('→ building whole project')
  bld.recurse('dylib')

def package(ctx):
  for file in glob.glob('net.r-ch.hatebu-instapaper/.DS_Store'):
    os.remove(file)
  for file in glob.glob('net.r-ch.hatebu-instapaper/*/.DS_Store'):
    os.remove(file)
  for file in glob.glob('net.r-ch.hatebu-instapaper/*/*/.DS_Store'):
    os.remove(file)
  for file in glob.glob('net.r-ch.hatebu-instapaper/*/*/*/.DS_Store'):
    os.remove(file)
  for file in glob.glob('net.r-ch.hatebu-instapaper/*/*/*/*/.DS_Store'):
    os.remove(file)
  Utils.exec_command("strip -x net.r-ch.hatebu-instapaper/Library/MobileSubstrate/DynamicLibraries/HatebuInstapaper.dylib")
  Utils.exec_command("ldid -S net.r-ch.hatebu-instapaper/Library/MobileSubstrate/DynamicLibraries/HatebuInstapaper.dylib")
  Utils.exec_command("dpkg-deb -b net.r-ch.hatebu-instapaper")
