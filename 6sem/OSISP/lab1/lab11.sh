#!/bin/bash

# Function to clear the screen
clear_screen() {
    echo -e "\033[2J" # Clear the screen
    echo -e "\033[H"  # Move cursor to home position (top-left)
}

# Function to hide cursor
hide_cursor() {
    echo -e "\033[?25l"
}

# Function to show cursor
show_cursor() {
    echo -e "\033[?25h"
}

# Function to display the time at a specific position
display_time() {
    local time_string=$(date +"%H:%M:%S")
    echo -e "\033[10;10H${time_string}" # Move to row 10, column 10
}

# Main loop
hide_cursor
while true; do
    clear_screen
    display_time
    sleep 1
done

# Show cursor when exiting (optional, won't be reached in this script)
show_cursor
