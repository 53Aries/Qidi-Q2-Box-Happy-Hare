#!/bin/bash

# 从文件/tmp/plr中读取数字
number=$(cat /home/mks/scripts/plr/plr_record)

# 确认number是数字
if ! [[ $number =~ ^[0-9]+$ ]] ; then
   echo "Error: No valid number found in /home/mks/scripts/plr/plr_record"
   exit 1
fi

# 检查是否存在gcode_lines字段
if grep -q "^gcode_lines = " /home/mks/printer_data/config/saved_variables.cfg; then
    # 如果存在，更新gcode_lines值
    sed -i "s/^gcode_lines = [0-9]*/gcode_lines = $number/" /home/mks/printer_data/config/saved_variables.cfg
else
    # 如果不存在，添加gcode_lines字段
    echo "gcode_lines = $number" >> /home/mks/printer_data/config/saved_variables.cfg
fi
