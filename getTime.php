<?php
       	$from=strtotime(date('Y-m-d'));
        $c= time();
            $t = $from;

            for ($i=1;$i<=(($c-$from)/60);$i++) {
            	//a[] 存放当天时间0 点到现在时间的每分钟的秒数   $d[] x 存放每一秒*1000 (页面需要数据毫秒？) 及 y 初始化为0
                 $a[] = $t;   
                //$a[] = array("x"=>$t*1000,"y"=>$this->getNumByMinute($t,$hosts));
                //按照年月日时分 
                 $d[date('YmdHi',$t)] = array('x'=>$t*1000,'y'=>0);
                $t += 60;
            }
            $timeR = array('min' => current($a),'max'=>end($a));

//echo var_export($timeR,true); 
//echo var_export($a,true); 

//echo var_export($d,true); 

//ip 转为数字
echo ip2long(str_replace('_','.','52_66_126_141'));
