<?php
   //test convert 转化特殊字符串  以便组装sql时 可以插入数据库 
  //  将'  转化为 \'
    $item = "/redirect?err_msg=offer\[445829\]%20checkGeoLimits%20failed%20at%20regionLimits%20when%20region=YE_Hadramawt_Sana'(134.35.115.144)-445829%20inactive%20and%20no%20redirecting%20offer%20given&aff_sub=AbCd4451f4621a74437081e597deb45f251eAzYx&aff_sub2=4556";
   
    if(strpos($item,'\'')){
	printf ("find ' ") ;
    }
    $escaped_item = mysql_escape_string($item);
    printf ("Escaped string: %s\n", $escaped_item);
?>
