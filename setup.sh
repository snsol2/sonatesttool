#!/bin/bash

inquire ()  {
  echo  -n "$1 [y/n/stop]? "
  read answer
  finish="-1"
  while [ "$finish" = '-1' ]
  do
    finish="1"
    if [ "$answer" = '' ];
    then
      answer=""
    else
      case $answer in
        y | Y | yes | YES ) answer="y";;
        n | N | no | NO ) answer="n";;
        stop | STOP ) answer="s";;
        *) finish="-1";
           echo    "Invalid response($answer) ---- ";
           echo -n 'please reenter [y/n/stop]? ';
           read answer;;
       esac
    fi
  done
}

echo "====================================="
echo "1. /etc/hosts modify." 
echo "   Add the OpenStack Controller IP." 
echo "   <OpenStack_Controller_IP>  controller"
echo "====================================="

inquire "Modify now?"
if [ "$answer" = "y" ]; then
  vi /etc/hosts
elif [ "$answer" = "n" ]; then
  echo "Display /etc/hosts"
  echo "====================================="
  cat /etc/hosts
  echo "====================================="
else
  echo "Invalid Answer($answer). Stop & Exit." ; exit;
fi



SYS_OS=$(uname -s)
echo "====================================="
echo "2. Install Package. OS($SYS_OS)." 
echo "   -  python-pip"
echo "   -  python-neutronclient"
echo "   -  python-novaclient"
echo "   -  python-keystoneclient"
echo "   -  oslo.config"
echo "   -  python-pexpect"
echo "====================================="

inquire "Install now?"
if [ "$answer" = "y" ]; then
  echo "Install the package."

  
  if [ "$SYS_OS" = "Linux" ]; then
    apt-get install python-pip
    apt-get install python-neutronclient
    apt-get install python-novaclient
    apt-get install python-keystoneclient
    apt-get install oslo.config
    apt-get install python-pexpect
  elif [ "$SYS_OS" = "Darwin" ]; then
    easy_install --upgrade six
    easy_install pip
    pip install python-neutronclient
    pip install python-novaclient
    pip install python-keystoneclient
    pip install oslo.config
    pip install pexpect
  else
    echo "Unknown OS($SYS_OS). Stop & Exit." ; exit; 
  fi
elif [ "$answer" = "n" ]; then
  echo "Skip the installation package."
else
  echo "Invalid Answer($answer). Stop & Exit." ; exit;
fi


echo "====================================="
echo "3. Set an environment variable. Current Shell($SHELL)." 
echo "   bash: export PYTHONPATH=`pwd`:."
echo "   csh:  setenv PYTHONPATH `pwd`:."
echo "====================================="
echo ""
echo "====================================="
echo " Installation is complete."
echo "====================================="

