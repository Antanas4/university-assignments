# This script is used to manage user's passwords and generate new ones
# -Create user: creates new account and adds new generated or user created prefferd password
# -GeneratePassword: generates a new password.
# -AddPassword: adds new password for an app
# -GetPassword: shows the password of the corresponding application
# -DeletePassword: deletes app's password
# -DeleteUser: deletes users and all of the associated passwords

export LC_CTYPE=C
passwordManager="/Users/antanas/uni/operacines_sistemos/nd2/PasswordManager.txt"
readMe="/Users/antanas/uni/operacines_sistemos/nd2/README.txt"
menu()
{
    echo "Password Manager"
    echo "1. Create user"
    echo "2. Generate password"
    echo "3. Get password"
    echo "4. Add password"
    echo "5. Delete password"
    echo "6. Deletes user"
    echo "8. Get information"
    echo "7. Exit"
    read -p "Enter your choice: " option

    case $option in
        1)
            CreateUser;;
        2)
            GeneratePassword
            ;;
        3)
            GetPassword
            ;;
        4)
            AddPassword
            ;;
        5)
            DeletePassword
            ;;
        
        6)
            DeleteUser
            ;;
        
        8)
            GetInfo
            ;;
        7)
            exit 0
            ;;
    esac
}

ValidateCharacterCount()
{
    local input="$1"

    if [[ $input =~ ^[0-9]$ && $input -ge 0 && $input -lt 10 ]]; then
        return 0
    else
        return 1
    fi
}
CreateUser()
{

    clear
    read -p "Enter username: " username

    if awk -v user="$username" '$1 == user && /^[^\t]/ { found=1; exit } END { exit !found }' "$passwordManager"; then
        echo "Username is already taken!"
    else
        echo "Create a passwrod for the user. 
        Enter 1 if you want to use your own password. 
        Enter 2 if you want to generate a password." 
        read passwordChoice
        if [[ $passwordChoice == 1 ]]; then
            read -p "Enter your password: " password
            echo -e "\n$username $password" >> "$passwordManager"
            echo "Account has been created successfully!"
        elif [[ $passwordChoice == 2 ]]; then
            GeneratePassword "$username"
        fi
    fi
}

GeneratePassword ()
{
    local specialCount
    local digitsCount
    local upperCaseCount
    local lowerCaseCount
    local passedUsername=$1

    read -p "Enter the number of special characters: " specialCount
    read -p "Enter the number of digits: " digitsCount
    read -p "Enter the number of upper case letters: " upperCaseCount
    read -p "Enter the number of lower case letters: " lowerCaseCount

    if (($specialCount + $digitsCount + $upperCaseCount + $lowerCaseCount < 21)); then
        if ValidateCharacterCount "$specialCount" && ValidateCharacterCount "$digitsCount" && ValidateCharacterCount "$upperCaseCount" && ValidateCharacterCount "$lowerCaseCount"; then
            specials=$( LC_CTYPE=C tr -dc '!@#$%^&*()_+=[]{}\|;:,<.>/?`~' </dev/urandom | head -c "$specialCount")
            digits=$( LC_CTYPE=C tr -dc  '0123456789' </dev/urandom | head -c "$digitsCount")
            lowerCase=$( LC_CTYPE=C tr -dc  'abcdefghijklmnopqrstuvwxyz' </dev/urandom | head -c "$lowerCaseCount")
            upperCase=$( LC_CTYPE=C tr -dc  'ABCDEFGHIJKLMNOPQRSTUVWXYZ' </dev/urandom | head -c "$upperCaseCount")

            password="$specials$digits$lowerCase$upperCase"

            password=$(echo "$password" | fold -w1 | gshuf | tr -d '\n')
            
            if [ -z "$passedUsername" ]; then

                echo "Password Generated Successfully: $password"
            else
                echo -e "\n$passedUsername $password" >> "$passwordManager"
            fi
        else
            echo "The number of special chars/digits/upper/lower case characters must be a single digit and lower than 10"

        fi
    else
        echo "Password length must be lower than 21 characters"
    fi
    
}


GetPassword()
{
    clear
    local username
    local userPassword
    local appName
    local appPassword

    echo "Please login to your account."
    read -p "Enter your username: " username
    read -p "Enter your Password: " userPassword
    
    lineNumber=$(awk -v user="$username" -v password="$userPassword" '$1 == user && $2 == password && /^[^\t]/ { print FNR; found=1; exit } END { if (!found) print -1 }' "$passwordManager")
    
    if [ "$lineNumber" -ne -1 ]; then

        read -p "Which app's password do you want to find? " appName

        output=$(awk -v startLine=$lineNumber '/'"$appName"'/ && NR > startLine {print; found=1; exit} /^$/ {if (!found) print "not found"}' "$passwordManager")
       
        
        if [ "$output" != "not found" ]; then
            appPassword=$(echo "$output" | awk '/'"$search_word"'/ {print $3}' | tr -d '\n')
            if [ -n "$appPassword" ]; then
                echo "Password for $appName: $appPassword"
            else
                echo "App name does not exist"
            fi
        else
            echo "App name does not exist"
        fi
        
    else
        echo "User does not exist!"
    fi
    
}

AddPassword()
{
    clear
    local username
    local userPassword
    local appName
    local appPassword

    echo "Please login to your account."
    read -p "Enter your username: " username
    read -p "Enter your Password: " userPassword
    
    lineNumber=$(awk -v user="$username" -v password="$userPassword" '$1 == user && $2 == password && /^[^\t]/ { print FNR; found=1; exit } END { if (!found) print -1 }' "$passwordManager")

    if [ "$lineNumber" -ne -1 ]; then

        read -p "Enter app name: " appName
        read -p "Enter app password: " appPassword
        newRecord="- $appName $appPassword"
        output=$(awk -v startLine=$lineNumber '/'"$appName"'/ && NR > startLine {print; found=1; exit} /^$/ {if (!found) print "not found"}' "$passwordManager")
       
        if [ "$output" != "not found" ]; then
            appPassword=$(echo "$output" | awk '/'"$search_word"'/ {print $3}' | tr -d '\n')
            if [ -n "$appPassword" ]; then
                echo "You already have a password for this"
                echo "Password for $appName: $appPassword"
            else
                lineNumber=$((lineNumber + 1))
                awk -v line="$lineNumber" -v record="$newRecord" 'NR == line {print record} {print}' "$passwordManager" > tmpfile && mv tmpfile "$passwordManager"
                echo "Password added successfully!"
            fi
        else
            echo "App name does not exist"
        fi
        
    else
        echo "User does not exist!"
    fi

}


DeletePassword()
{
    clear
    local username
    local userPassword
    local appName
    local appPassword

    echo "Please login to your account."
    read -p "Enter your username: " username
    read -p "Enter your Password: " userPassword
    
    lineNumber=$(awk -v user="$username" -v password="$userPassword" '$1 == user && $2 == password && /^[^\t]/ { print FNR; found=1; exit } END { if (!found) print -1 }' "$passwordManager")
    
    if [ "$lineNumber" -ne -1 ]; then
        echo "Username found at line $lineNumber."
        read -p "Which app's password do you want to delete? " appName
        appLineNumber=$(awk -v startLine=$lineNumber '/'"$appName"'/ && NR > startLine { print FNR; found=1; exit } END { if (!found) print -1 }' "$passwordManager")

        if [ "$appLineNumber" -ne -1 ]; then
            sed -i '' "${appLineNumber}d" "$passwordManager"
            echo "Password for "$appName" deleted successfully!"
        else
            echo "App name does not exist"
        fi

    else
        echo "User does not exist!"
    fi
}

DeleteUser() {
    clear
    local username
    local userPassword
    local appName
    local appPassword

    echo "Please login to your account."
    read -p "Enter your username: " username
    read -p "Enter your Password: " userPassword

    startLine=$(awk -v user="$username" -v password="$userPassword" '$1 == user && $2 == password && /^[^\t]/ { print FNR; found=1; exit } END { if (!found) print -1 }' "$passwordManager")

    if [ "$startLine" -ne -1 ]; then
        endLine=$(awk -v startLine="$startLine" '/^$/ && NR > startLine {print FNR; exit} END {if (NR <= startLine) print startLine + 1}' "$passwordManager")
        awk -v start="$startLine" -v end="$endLine" 'NR >= start && NR <= end {next} 1' "$passwordManager" > temp_file && mv temp_file "$passwordManager"

        if [ "$endLine" -eq $(wc -l < "$passwordManager") ]; then
            sed -i "$(($startLine - 1))d" "$passwordManager"
            sed -i "$(($endLine + 1))d" "$passwordManager"
        fi

        echo "User and associated passwords deleted successfully."
    else
        echo "User does not exist!"
    fi
}

GetInfo()
{
    cat "$readMe"
}


while true; do
    menu
done
