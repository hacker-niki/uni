#!/bin/bash

clear_screen() {
    echo -e "\033[2J"
    echo -e "\033[H"
}

hide_cursor() {
    echo -e "\033[?25l"
}

declare -A digits

digits[0,0]=" _ "
digits[0,1]="| |"
digits[0,2]="|_|"
digits[1,0]="   "
digits[1,1]=" | "
digits[1,2]=" | "
digits[2,0]=" _ "
digits[2,1]=" _|"
digits[2,2]="|_ "
digits[3,0]=" _ "
digits[3,1]=" _|"
digits[3,2]=" _|"
digits[4,0]="   "
digits[4,1]="|_|"
digits[4,2]="  |"
digits[5,0]=" _ "
digits[5,1]="|_ "
digits[5,2]=" _|"
digits[6,0]=" _ "
digits[6,1]="|_ "
digits[6,2]="|_|"
digits[7,0]=" _ "
digits[7,1]="  |"
digits[7,2]="  |"
digits[8,0]=" _ "
digits[8,1]="|_|"
digits[8,2]="|_|"
digits[9,0]=" _ "
digits[9,1]="|_|"
digits[9,2]=" _|"

a=45245    
m=24563425657
X=$(date +%s) 

random() {
	X=$(( (a * X) % m))
}

get_random_position() {	
    local rows=$(tput lines) 
    local cols=$(tput cols)     
    
    local max_row=$((rows - 4)) 
    local max_col=$((cols - 22))

    echo $(( $X % max_row + 1)) $(( $X % max_col + 1))
}

display_time() {
    local time_string=$(date +"%H%M%S")
    clear_screen

    line0=""
    line1=""
    line2=""

    for ((i=0; i<${#time_string}; i++)); do
        digit=${time_string:i:1}
        line0+="${digits[$digit,0]}"
        line1+="${digits[$digit,1]}"
        line2+="${digits[$digit,2]}"

		if [[ $(($i % 2)) == 1 && ($i < 30) ]]; then
			 line0+="   "
			 line1+=" × "
			 line2+=" × "
		fi
    done

    echo -e "\033[$1;$2H$line0"
    echo -e "\033[$(( $1 + 1 ));$2H$line1"
    echo -e "\033[$(( $1 + 2 ));$2H$line2"
}

hide_cursor

while true; do
	random
	read row col < <(get_random_position)
	for ((j=0; j<5; j++)); do
    	display_time $row $col	
    	sleep 1
	done
done
