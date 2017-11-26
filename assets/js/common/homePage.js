'use strict';

define(['jquery','bootstrap'], function($){
     var firstTime = 0, firstTime1 = 0,  firstTime2 = 0, firstTime3=0;
     $(".fixed-bar").addClass('fadeOutUp');
      //var hottedGpLength = 0, latestGpLength = 0, allGpLength = 0;
      //var hottedElement = $(".hottest");
      //var latestElement = $(".latest");
      //var allGpElement = $(".all-groups");

      //var normalHomePage =  true;
      var windowHeight = $(window).height();

      //if (latestElement.length == 0){
     //   normalHomePage = false;
      //}else{
      //  latestGpLength = latestElement.offset().top;
      //  allGpLength = allGpElement.offset().top;
      //  hottedGpLength = hottedElement.offset().top;
      //}

    $(window).scroll(function () {

        var headerLength = $(".splash").outerHeight();

        var scrollLength = $(document).scrollTop();
        /*if ((latestGpLength !== 0) &&
              (firstTime1 == 0) &&
              (scrollLength > (latestGpLength - windowHeight + 70))){
            $(".latest a img").addClass("animated flash");
            firstTime1 = 1;
        }

        if ((allGpLength !== 0) &&
              (firstTime2 == 0) &&
              (scrollLength > (allGpLength - windowHeight + 70))){
            $(".all-groups a img").addClass("animated flash");
            firstTime2++;
        }*/

       if (scrollLength > headerLength){
           $(".fixed-bar").removeClass('fadeOutUp');
           $(".fixed-bar").addClass('fadeInDown');

           if (!firstTime){
            $(".fixed-bar").css('display','block');
            firstTime++;
           }
       }else{
           $(".fixed-bar").removeClass('fadeInDown');
           $(".fixed-bar").addClass('fadeOutUp');
       }
    });
});