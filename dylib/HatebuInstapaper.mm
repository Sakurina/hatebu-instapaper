#import "CaptainHook.h"
#import <UIKit/UIKit.h>

#define InstapaperIsInstalled ([[UIApplication sharedApplication] canOpenURL:[NSURL URLWithString:@"ihttp://localhost"]])

CHDeclareClass(WebViewController);

CHMethod1(void, WebViewController, openButonPushed, id, sender) {
  if (!InstapaperIsInstalled) {
    CHSuper1(WebViewController, openButonPushed, sender);
    return;
  }

  NSString* url = [[self webView] stringByEvaluatingJavaScriptFromString:@"location.href"];
  UIActionSheet* as = [[UIActionSheet alloc] initWithTitle:url
                                                  delegate:self
                                         cancelButtonTitle:@"キャンセル"
                                    destructiveButtonTitle:nil
                                         otherButtonTitles:@"Safariで開く", @"Instapaperに送信", nil];
  [as showFromToolbar:[self toolbar]];
}

CHMethod2(void, WebViewController, actionSheet, id, as, clickedButtonAtIndex, int, index) {
  if (!InstapaperIsInstalled) {
    CHSuper2(WebViewController, actionSheet, as, clickedButtonAtIndex, index);
    return;
  }

  NSURL* url = nil;
  switch (index) {
    case 0:
      url = [NSURL URLWithString:[as title]];
      [[UIApplication sharedApplication] openURL:url];
      break;
    case 1:
      url = [NSURL URLWithString:[@"i" stringByAppendingString:[as title]]];
      [[UIApplication sharedApplication] openURL:url];
      break;
  }
  [as release];
}

CHConstructor {
  CHAutoreleasePoolForScope();

  CHLoadLateClass(WebViewController);
  CHHook1(WebViewController, openButonPushed);
  CHHook2(WebViewController, actionSheet, clickedButtonAtIndex);
}
