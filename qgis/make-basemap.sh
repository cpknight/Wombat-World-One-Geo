#!/bin/bash

# Echo current date and time in YYYYMMDD HHMMSS format
CURRENT_DATETIME=$(date +"%Y%m%d %H%M%S")
echo "Current date and time: $CURRENT_DATETIME"

# Save date and time as separate variables
YYYYMMDD=$(date +"%Y%m%d")
HHMMSS=$(date +"%H%M%S")

# Function to create a temporary filename with date, time, and random component
create_temp_filename() {
    local random_component=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
    echo "/tmp/basemap-temp-$YYYYMMDD-$HHMMSS-$random_component.png"
}

# Cleanup function to remove all temp files with the common prefix
cleanup_temp_files() {
    rm -f /tmp/basemap-temp-*.png
}

# Clean up any old temporary files at the start
cleanup_temp_files

# Prompt user to create a new basemap TIFF
read -p "Create a new basemap TIFF for $YYYYMMDD $HHMMSS? (Yes/No): " answer

# Convert answer to lowercase for case-insensitive comparison
answer=$(echo "$answer" | tr '[:upper:]' '[:lower:]')

if [ "$answer" == "yes" ]; then
    # Generate temporary filename
    TEMP_OUTPUT=$(create_temp_filename)
    echo "Temporary output file: $TEMP_OUTPUT"

    # Your conversion code here:
/home/cpknight/Applications/unmined-cli_0.19.48-dev_linux-x64/unmined-cli image render \
--trim \
--zoom 0 \
--world "/home/cpknight/.minecraft/saves/W0mbit World 1/" \
--output "$TEMP_OUTPUT"

    # Verify that temporary output file exists
    if [ ! -f "$TEMP_OUTPUT" ]; then
        echo "Error: Temporary output file $TEMP_OUTPUT does not exist."
        cleanup_temp_files
        exit 1
    fi

    # Display the output file
    kitty +kitten icat $TEMP_OUTPUT

    # Prompt to locate origin pixels
    read -p "Locate the origin pixels using GIMP? (Yes/No): " gimp_answer
    gimp_answer=$(echo "$gimp_answer" | tr '[:upper:]' '[:lower:]')

    if [ "$gimp_answer" == "yes" ]; then
        # Launch GIMP with the temporary output file
        gimp $TEMP_OUTPUT

        # Wait for user input for X and Y pixel values
        read -p "Enter X pixel value: " originX
        read -p "Enter Y pixel value: " originY

        # Obtain width and height of the temporary output file
width=$(exiv2 "$TEMP_OUTPUT" 2>/dev/null | grep 'Image size' | awk '{print $4}')
height=$(exiv2 "$TEMP_OUTPUT" 2>/dev/null | grep 'Image size' | awk '{print $6}')

        # Display the variables
        echo "Width: $width, Height: $height, OriginX: $originX, OriginY: $originY"

        # Calculate new variables
        v1=$((-$originX))  # Reverse the sign of originX
        v2=$originY        # Keep the sign of originY the same
        v3=$(($width + $v1)) # Add reversed originX to width
        v4=$(($height - $v2)) # Subtract originY from height
        v4r=$((-$v4))

        # Display the calculated values
        echo "V1: $v1, V2: $v2, V3: $v3, V4: $v4r"

        # Ask to continue generating TIFF
        read -p "Continue to generate TIFF? (Yes/No): " continue_answer
        continue_answer=$(echo "$continue_answer" | tr '[:upper:]' '[:lower:]')

        if [ "$continue_answer" == "yes" ]; then
            # Echo the filename for the new TIFF
            echo "Generating basemap-wombat-world-$YYYYMMDD-$HHMMSS.tif"

            # TIFF generation code
            # -9788 9886 13188 -5106
	    gdal_translate -a_ullr $v1 $v2 $v3 $v4r $TEMP_OUTPUT basemap-wombat-world-$YYYYMMDD-$HHMMSS.tif 
        fi
    fi

    # Clean up temporary files before exit
    cleanup_temp_files
    echo "Cleanup completed. Script exiting."
else
    echo "Script terminated by user."
    cleanup_temp_files
    exit 0
fi
