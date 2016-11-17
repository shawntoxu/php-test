<?php

// 测试正则匹配 
$msg='---i--[BUG]logic queue order maybe wrong, expectLogicOffset -ERROR---i[BUG]logic queue order maybe wrong, expectLogicOffset';
$errorKeys='/consume queue can not write|logic queue order maybe wrong, expectLogicOffset/i';
//$errorKeys='/[BUG]consume queue can not write|ERROR|[BUG]logic queue order maybe wrong, expectLogicOffset|so mark disk full|create mmap timeout|[BUG]put commit log position info to|[BUG]consume queue can not write|ScheduleMessageService, executeOnTimeUp exception/i';

  if (preg_match($errorKeys, $msg)){
		
	echo "ok";

 }
