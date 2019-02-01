function spc() {
 user=""
 pass=""
  if [ $1 = "help" ];then
  	echo "spc login: User needs to do this before going forward with anything else. Requires Username and Password"
  	echo "spc register: To be done after login. For first time user-initialize Private Key, Encryption Schema, Sharing key. For old user: enter previous Private key, encryotion schema and sharing key to authenticate "
  	echo "spc observe: Go into the directory that you want to sync and then use this command."
  	echo "spc sync: To be done after observe. Used to sync the observed directory and server"
  	echo "spc rec <file_name> user_A : To be used by user to receive <file_name> from user_A"
  	echo "spc send <file_name> user_B : To be used to send <file_name> to user_B"
  	echo "spc version:view version of SPC"
  	echo "spc server: prints public info about server"
  	echo "spc status: print prints sync status of each of the files on server and observed directory"
  	echo "spc en-de list:show all supported encryption schemas"
  	echo "spc en-de update:update encryption schema, private key and sharing key"
  	echo "spc en-de show:shows present encryption schema"
  elif [ $1 = "version" ];then
  	echo "ver.1.2.0"	
  elif [ $1 = "status" ];then
  	echo "lets do it"

  elif [ $1 = "login" ];then
  	login 	
  elif [ $1 = "upload" ];then
  	
  	touch ~/upload-cookies.txt
  	val=$(md5sum ~/login.log | cut -d " " -f 1)
  	if [ $val = "d41d8cd98f00b204e9800998ecf8427e" ];then
  		if [ -f ~/observe.txt ];then
  		if [ -f $2 ];then
  			file=$2
  			a=$(dirname $(readlink -f $2))
  			b=$(cat ~/observe.txt)
  			if [ $a = $b ];then
  				direc=$(echo ".")
  			else
  			direc=$(echo ${a//$b/})
  		fi
  			fname=$(basename $file)
  				first=$(echo $fname | cut -d "." -f 1)
  				ftype=$(echo $fname | cut -d "." -f 2)
  				if [ $first = $ftype ];then
  					ftype=null
  				fi
  				var=$(md5sum $file | cut -d " " -f 1)
  				echo $first $ftype $file $direc $var
  				upload $first $ftype $file $direc $var
  		else
  			echo Bad file credentials		
  		fi
  	else
  		echo observe first using spc observe
  	fi
  	fi
  	rm -r ~/upload-cookies.txt
  elif [ $1 = "directory_upload" ];then
  	touch ~/upload-cookies.txt
  	val=$(md5sum ~/login.log | cut -d " " -f 1)
  	if [ $val = "d41d8cd98f00b204e9800998ecf8427e" ];then
  		if [ -f ~/observe.txt ];then
  		echo " "
  		if [ -d $2 ];then
  			find $2 -type f | while read file;
  			do 
  				 a=$(dirname $(readlink -f $file))
  			b=$(cat ~/observe.txt)
  				if [ $a = $b ];then
  				direc=$(echo ".")
  			else
  			direc=$(echo ${a//$b/})
  		fi
  				fname=$(basename $file)
  				if [ $fname = "~/login-cookies.txt" ];then
  					continue
  				fi
  				first=$(echo $fname | cut -d "." -f 1)
  				ftype=$(echo $fname | cut -d "." -f 2)
  				if [ $first = $ftype ];then
  					ftype=null
  				fi
  				var=$(cat $file | md5sum | cut -d " " -f 1)
  				echo $first $ftype $file $direc
  				upload $first $ftype $file $direc $var	
  			done
  		else 
  			echo Not a directory	
  		fi
  		else
  		echo observe first using spc observe
  	fi
  	fi

  	rm -r ~/upload-cookies.txt
  elif [ $1 = "observe" ];then
  	pwd > ~/observe.txt
  elif [ $1 = "sync" ];then
  	touch ~/upload-cookies.txt
  	if [ -f ~/login-cookies.txt ];then
  	val=$(md5sum ~/login.log | cut -d " " -f 1)
  	if [ $val = "d41d8cd98f00b204e9800998ecf8427e" ];then
  		if [ -f ~/observe.txt ];then
  		echo " "
  			x=$(cat ~/observe.txt)
  			export -f sync_helper
  			export -f search
  			export -f delete
  			export -f upload
  			find $x -type f -exec bash -c 'sync_helper "{}"' \;
  			find $x -type f |while read file;
  			do
  				rm $file
  			done
  			curl -b ~/login-cookies.txt http://127.0.0.1:8000/data_json/ > ~/data.json
  			sed 's/&#39;/"/g' ~/data.json > ~/data
  			python3 ~/sync.py
  			if [ -f register.log.enc ];then
  				rm register.log.enc
  			fi
  			if [ $(head -n 2  ~/enc.txt | tail -n 1) = "1" ];then
		  		key=$(head -n 1 ~/enc.txt)
		  		key=$(echo $key |md5sum)
		  		key=${key:0:32}
		  		iv=$key
		  		#iv=${iv:0:32}
		  		find -type f | while read file;
		  		do
		  			encpath=$(readlink -f $file)
		  			decpath=${encpath%.enc}
		  			openssl enc -aes-128-cbc -in $encpath -out $decpath -d -a -nosalt -K $key -iv $iv
					rm $encpath
				done
			elif [ $(head -n 2  ~/enc.txt | tail -n 1) = "2" ];then
	            key=$(head -n 1 ~/enc.txt)
	            key=$(echo $key |md5sum)
	            key=${key:0:32}
	            key="$key${key:0:16}"
	            iv=${key:0:16}
	            find -type f | while read file;
	            do
	        
	              encpath=$(readlink -f $file)
	              decpath=${encpath%.enc}
	              openssl enc -des3 -in $encpath -out $decpath -d -a -nosalt -K $key -iv $iv
	           		rm $encpath
	            done
	        elif [ $(head -n 2  ~/enc.txt | tail -n 1) = "3" ];then
	            key=$(head -n 1 ~/enc.txt)
	            key=$(echo $key |md5sum)
	            key=${key:0:16}
	            iv=$key
	            find -type f | while read file;
	            do
	              	encpath=$(readlink -f $file)
		            decpath=${encpath%.enc}
		            openssl enc -rc2-64-cbc -in $encpath -out $decpath -d -a -nosalt -K $key -iv $iv
			        rm $encpath
			    done
			fi



  		else
  		echo observe first using spc observe
  	fi
  	fi
  	rm -r  ~/upload-cookies.txt
  else
  	echo login first using spc login
  fi
elif [ $1 = "logout" ];then
	if [ -f ~/login-cookies.txt ];then
		rm  ~/login-cookies.txt
			if [ -f ~/enc.txt ];then
				rm  ~/enc.txt
			fi
	else
	echo login first
	fi
elif [ $1 = "register" ];then
	if [ -f ~/login-cookies.txt ];then
		if [ -f ~/enc.txt ];then
			rm ~/enc.txt
		fi
		read -p "Enter encyption key: " key
		read -p "Encryption schema (1,2,3): " schema
		read -p "sharing key: " shar_key
		echo "do remember these keys afterwards"
		echo $key | cat >> ~/enc.txt
		echo $schema | cat >> ~/enc.txt
		echo $shar_key | cat >> ~/enc.txt
		key=$(echo $key | md5sum | cut -d " " -f 1)
		schema=$(echo $schema | md5sum | cut -d " " -f 1)
		shar_key=$(echo $shar_key | md5sum | cut -d " " -f 1)
		bool=$(register $key $schema $shar_key)
		if [ $bool = "1" ];then
			echo wrong details provided... try again
			rm ~/enc.txt
		elif [ $bool = "2" ];then
      python3 rsa_gen.py
      n=$(head -n 1 ~/rsa.txt)
      e=$(head -n 2 ~/rsa.txt |tail -n 1)
      d=$(tail -n 1 ~/rsa.txt)
      rm ~/rsa.txt
      echo $d > ~/temp.txt
      echo $d
      if [ $(head -n 2  ~/enc.txt | tail -n 1) = "1" ];then
      key=$(head -n 1 ~/enc.txt)
      key=$(echo $key |md5sum)
      key=${key:0:32}
      iv=$key
      openssl enc -aes-128-cbc -in ~/temp.txt -out ~/temp.txt.enc -e -a -nosalt -K $key -iv $iv
      
      fi
      d=$(cat ~/temp.txt.enc)
      #echo $d
      #d2=${d//,\n|}
      d2=$(echo $d | tr '\n' '|')
      echo $d2
      #echo "$d2"
      #d3=$(echo $d2 | tr '|' '\n')
      #echo d3
      #echo "d3"
      update_key $n $e "$d2"

      rm ~/temp.txt ~/temp.txt.enc  
			echo successfully register 
    else
    echo successfully register
    fi
	else
		echo login first using spc login
	fi
elif [ $1 = "rec" ];then
  if [ -f ~/login-cookies.txt ];then
    a=$2
    val=$(get_a $a)
    val=$(echo ${val//lol1234567890/})
    val=$(echo ${val//end1234567890/})
    n=$(echo $val | awk -F"lol0987654321" '{ print $1}')
    e=$(echo $val | awk -F"lol0987654321" '{ print $2}')
    mess=$(tail -n 1 ~/enc.txt)
    echo $mess
    message=$(echo $mess | md5sum | cut -d " " -f 1) 
    echo $message
    echo $message $n $e
    message=$(python3 ~/sbwa.py $message $n $e)
    recieve $2 $message $3
    sleep 100
    down


  else
  echo login first
  fi
elif [ $1 = "send" ];then
  if [ -f ~/login-cookies.txt ];then
    val=$(dec_key)
    val=$(echo ${val//lol1234567890/})
    val=$(echo ${val//end1234567890/})
    d=$(echo $val | awk -F"lol0987654321" '{ print $1}')
    n=$(echo $val | awk -F"lol0987654321" '{ print $2}')
    d=${d%|}
    echo $d abcde
    echo "$d" > ~/temp1.txt.enc
    #echo $d
    if [ $(head -n 2  ~/enc.txt | tail -n 1) = "1" ];then
      key=$(head -n 1 ~/enc.txt)
      key=$(echo $key | md5sum | cut -d " " -f 1)
      key=${key:0:32}
      iv=$key

      openssl enc -aes-128-cbc -in ~/temp1.txt.enc -out ~/temp1.txt -d -a -nosalt -K $key -iv $iv
      
      fi

      d=$(cat ~/temp1.txt)
      echo "$d"
      rm ~/temp1.txt ~/temp1.txt.enc
      #echo $d
      val=$(fetch_key $2)
      val=$(echo ${val//lol1234567890/})
      val=$(echo ${val//newend3456789012/})
      userb=$(echo $val | awk -F"lol0987654321" '{ print $1}')
      
      f=$(echo $val | awk -F"lol0987654321" '{ print $2}')
      file=$(echo $f | awk -F"end1234567890" '{ print $1}')
      sofbwa=$(echo $f | awk -F"end1234567890" '{ print $2}')
      shared_key=$(python3 ~/dec.py $sofbwa $n $d)
      file=$(readlink -f file)
      openssl enc -aes-128-cbc -in $file -out "$file.enc" -e -a -nosalt -K $shared_key -iv $shared_key
      efile="$file.enc"
      if [ -f ~/observe.txt ];then
      if [ -f $efile ];then
        file=$efile
        a=$(dirname $(readlink -f $file))
        b=$(cat ~/observe.txt)
        if [ $a = $b ];then
          direc=$(echo ".")
        else
        direc=$(echo ${a//$b/})
      fi
        fname=$(basename $file)
          first=$(echo $fname | cut -d "." -f 1)
          ftype=$(echo $fname | cut -d "." -f 2)
          if [ $first = $ftype ];then
            ftype=null
          fi
          var=$(md5sum $file | cut -d " " -f 1)
          echo $first $ftype $file $direc $var
          share_upload $first $ftype $file $direc $var $2
          sleep 100
          remover_share_upload $first $ftype $direc $var $2
      else
        echo requested file not available
      fi
    else
      echo observe first using spc observe
    fi
      fi

  else 
  	echo Invalid command	 	
  fi
}

function upload() {
	c="@"
  	value=$(curl -v -c ~/upload-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/file_add/ | grep -o "value=['\"][^'\"]*")
  	value=$(echo $value | cut -d "'" -f 2)
  	if [ $(head -n 2  ~/enc.txt | tail -n 1) = "1" ];then
  		key=$(head -n 1 ~/enc.txt)
  		key=$(echo $key |md5sum)
  		key=${key:0:32}
  		iv=$key
  		#iv=${iv:0:32}
  		path=$(readlink -f $3)
  		
  		openssl enc -aes-128-cbc -in $path -out ""$path".enc" -e -a -nosalt -K $key -iv $iv
		newrel=""$3".enc"
	elif [ $(head -n 2  ~/enc.txt | tail -n 1) = "2" ];then
	      key=$(head -n 1 ~/enc.txt)
	      key=$(echo $key |md5sum)
	      key=${key:0:32}
	      key="$key${key:0:16}"
	      iv=${key:0:16}
	      #iv=${iv:0:32}
	      path=$(readlink -f $3)



	      openssl enc -des3 -in $path -out ""$path".enc" -e -a -nosalt -K $key -iv $iv
    	newrel=""$3".enc"
	 #echo "$path is uploaded"
   	elif [ $(head -n 2  ~/enc.txt | tail -n 1) = "3" ];then
    	  key=$(head -n 1 ~/enc.txt)
      	key=$(echo $key |md5sum)
      	key=${key:0:16}
      	iv=$key
      	#iv=${iv:0:32}
      	path=$(readlink -f $3)
      
      openssl enc -rc2-64-cbc -in $path -out ""$path".enc" -e -a -nosalt -K $key -iv $iv
    newrel=""$3".enc"
	#newrel=$3
	
	fi

  	curl -v -c ~/upload-cookies.txt -b ~/upload-cookies.txt -H "Content-Disposition: attachment;" -F "file_name=$1" -F "md5sum=$5" -F "file_type=$2" -F "file_file=@$newrel" -F "file_address=$4" -F "csrfmiddlewaretoken=$value" http://127.0.0.1:8000/file_add/ > upload.log
  	
  	echo "$path is uploaded successfully"
}
function login() {
	read -p "Enter Username: " username
  	read -p "Enter Password: " -s password
  	data=$(curl -s -c ~/login-cookies.txt http://127.0.0.1:8000/login/ | grep -o "name=['\"]csrfmiddlewaretoken['\"] value=['\"][^'\"]*" | sed -e "s/name='//" -e "s/' value='/=/")\&username=$username\&password=$password
  	curl -b ~/login-cookies.txt -c ~/login-cookies.txt -d $data -X POST -H 'Content-Type: application/x-www-form-urlencoded' http://127.0.0.1:8000/login/ > ~/login.log
  	user=$username
  	pass=$password 	
  	val=$(md5sum ~/login.log | cut -d " " -f 1)
  	if [ $val = "d41d8cd98f00b204e9800998ecf8427e" ];then
  		echo " "
  		echo Logged in successfully
  	else
  		echo " "
  		echo Inavalid Login credentials....Check ~/login.log
  		rm ~/login-cookies.txt
  	fi		
}
function search() {
  	value=$(curl -v -c search-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/file_search/ | grep -o "value=['\"][^'\"]*")
  	value=$(echo $value | cut -d "'" -f 2)
  	curl -v -c search-cookies.txt -b search-cookies.txt -H "Content-Disposition: attachment;" -d "file_name=$1" -d "file_type=$2" -d "md5sum=$4" -d "file_address=$3" -d "csrfmiddlewaretoken=$value" http://127.0.0.1:8000/file_search/ > search.log
  	val=$(grep -rl yes search.log)
  	if [ $val = "search.log" ];then
  		echo 1
  	else
  	
  		echo 0
  	fi
}
function delete() {
	c="@"
  	value=$(curl -v -c delete-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/file_delete/ | grep -o "value=['\"][^'\"]*")
  	value=$(echo $value | cut -d "'" -f 2)
  	curl -v -c delete-cookies.txt -b delete-cookies.txt -H "Content-Disposition: attachment;" -F "file_name=$1" -F "file_type=$2" -F "file_address=$3" -F "csrfmiddlewaretoken=$value" http://127.0.0.1:8000/file_delete/
  	rm -r delete-cookies.txt	
}
function sync_helper() {
  			a=$(dirname $(readlink -f $1))
  			b=$(cat ~/observe.txt)
  				if [ $a = $b ];then
  				direc=$(echo ".")
  			else
  			direc=$(echo ${a//$b/})
  		fi
  				fname=$(basename $1)
  				if [ $fname = "login-cookies.txt" ] || [ $fname = "login.log" ] || [ $fname = "search-cookies.txt" ] || [ $fname = "upload-cookies.txt" ];then
  					return
  				fi
  				first=$(echo $fname | cut -d "." -f 1)
  				ftype=$(echo $fname | cut -d "." -f 2)
  				if [ $first = $ftype ];then
  					ftype=null
  				fi
  				var=$(md5sum $1 | cut -d " " -f 1)
  				echo $first $ftype $direc $var 3
  				bool=$(search $first $ftype $direc $var)
  				echo $bool
  				if [ $bool = "1" ];then
  					abc=$(echo Do you want to update the file $1 )
  					echo $abc
  					read -p "press y or n: " val
  					if [ $val = "y" ];then
  						delete $first $ftype $direc
  						echo $first $ftype $direc $var 1
  						upload $first $ftype $1 $direc $var
  					elif [ $val = "n" ]; then
  						return
  					else
  						echo nothing done to the file due to bad command
  					fi
  				elif [ $bool = "2" ]; then
  						return
  				else
  					echo $first $ftype $direc $var 1
  					upload $first $ftype $1 $direc $var
  				fi
}
function register() {
	c="@"
  	value=$(curl -v -c register-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/register/ | grep -o "value=['\"][^'\"]*")
  	value=$(echo $value | cut -d "'" -f 2)
  	curl -v -c register-cookies.txt -b register-cookies.txt -H "Content-Disposition: attachment;" -F "private_key=$1" -F "schema=$2" -F "shared_key=$3" -F "csrfmiddlewaretoken=$value" http://127.0.0.1:8000/register/ > register.log
  	val=$(grep -rl yes register.log)
    v=$(grep -rl abc register.log)
  	if [ $val = "register.log" ];then
  		echo 1
  	elif [ $v = "register.log" ];then
      echo 2
    else
  		echo 0
  	fi
  	rm -r register-cookies.txt 
}
function update_key() {
  c="@"
  echo hi
    value=$(curl -v -c ~/update-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/update_key/ | grep -o "value=['\"][^'\"]*")
    value=$(echo $value | cut -d "'" -f 2)
    echo "$3"
    curl -v -c ~/update-cookies.txt -b ~/update-cookies.txt -H "Content-Disposition: attachment;" -F "n=$1" -F "e=$2" -F "d=$3" -F "csrfmiddlewaretoken=$value" http://127.0.0.1:8000/update_key/  > a.log
    rm a.log ~/update-cookies.txt
}
function recieve() {
  c="@"
    value=$(curl -v -c ~/rec-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/rec/ | grep -o "value=['\"][^'\"]*")
    value=$(echo $value | cut -d "'" -f 2)
    curl -v -c ~/rec-cookies.txt -b ~/rec-cookies.txt -H "Content-Disposition: attachment;" -F "usera=$1" -F "sofbwa=$2" -F "file=$3" -F "csrfmiddlewaretoken=$value" http://127.0.0.1:8000/rec/  > a.log
    rm a.log ~/rec-cookies.txt
}
function get_a() {
  c="@"
    value=$(curl -v -c ~/get_a-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/key_detail/ | grep -o "value=['\"][^'\"]*")
    value=$(echo $value | cut -d "'" -f 2)
    curl -v -c ~/get_a-cookies.txt -b ~/get_a-cookies.txt -H "Content-Disposition: attachment;" -F "usera=$1" -F "csrfmiddlewaretoken=$value" http://127.0.0.1:8000/key_detail/  > a.log
    grep lol1234567890 a.log
    rm ~/get_a-cookies.txt a.log
}
function dec_key() {
    c="@"
    curl -c ~/dec_key-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/dky_detail/  > a.log
    grep lol1234567890 a.log
    rm ~/dec_key-cookies.txt a.log
}

function fetch_key() {
    c="@"
    value=$(curl -v -c ~/m_b-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/m_b/ | grep -o "value=['\"][^'\"]*")
    value=$(echo $value | cut -d "'" -f 2)
    curl -v -c ~/m_b-cookies.txt -b ~/m_b-cookies.txt -H "Content-Disposition: attachment;" -F "usera=$1" -F "csrfmiddlewaretoken=$value" http://127.0.0.1:8000/m_b/  > a.log
    grep lol1234567890 a.log
    rm ~/m_b-cookies.txt a.log
}

function share_upload() {
  c="@"
    value=$(curl -v -c ~/share_upload-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/share/ | grep -o "value=['\"][^'\"]*")
    value=$(echo $value | cut -d "'" -f 2)
    curl -v -c ~/share_upload-cookies.txt -b ~/share_upload-cookies.txt -H "Content-Disposition: attachment;" -F "file_name=$1" -F "md5sum=$5" -F "file_type=$2" -F "file_file=@$3" -F "file_address=$4" -F "userb=$6" -F "csrfmiddlewaretoken=$value" http://127.0.0.1:8000/share/ > upload.log
    #rm $newrel
    echo file uploaded successfully
    rm upload.log share_upload-cookies.txt
}
function remover_share_upload() {
  c="@"
    value=$(curl -v -c ~/share_upload-cookies.txt -b ~/login-cookies.txt http://127.0.0.1:8000/remove/ | grep -o "value=['\"][^'\"]*")
    value=$(echo $value | cut -d "'" -f 2)
    curl -v -c ~/share_upload-cookies.txt -b ~/share_upload-cookies.txt -H "Content-Disposition: attachment;" -F "file_name=$1" -F "md5sum=$4" -F "file_type=$2"  -F "file_address=$3" -F "userb=$5" -F "csrfmiddlewaretoken=$value" http://127.0.0.1:8000/remove/ > upload.log
    #rm $newrel
    echo file uploaded successfully
    rm upload.log share_upload-cookies.txt
}

function down() {
        curl -b ~/login-cookies.txt http://127.0.0.1:8000/share_data1/ > ~/shared_data.json
        sed 's/&#39;/"/g' ~/shared_data.json > ~/data
        python3 ~/sync.py       
}