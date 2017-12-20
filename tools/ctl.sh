#!/bin/bash
#
# pc @ 20171220
# service control.
# Notice: on CentOS6, python2.6 is the default option.

appname='navigation'
d_src="/opt/src/${appname}"
d_root="/data/www/${appname}.test.com"
d_target="${d_root}/src_$(date +%Y%m%d_%H%M%S)"
d_link="${d_root}/latest"
f_sqlite_src='/data/db/sqlite/db.sqlite3'
f_sqlite_dest="${d_target}/db.sqlite3"
f_secret_key="/root/.django.secret_key.${appname}"
py27='/usr/local/bin/python2.7'

function create_secret_key(){
    echo '[+] set default secret_key for project.latest'
    python -c '
import random,string;
SECRET_KEY = "".join(
    [random.SystemRandom().choice(
        "{0}{1}{2}".format(
            string.ascii_letters, string.digits, string.punctuation
            )
        ) for i in range(50)]);
print "{0}".format(SECRET_KEY);
' > ${f_secret_key}
    echo "[-] saved to: ${f_secret_key}"
}

function update_django_settings(){
    echo '[+] replace secret_key, ALLOWED_HOSTS, DEBUG off.'
    s_key="'$(cat ${f_secret_key})'"
    sed -i -e "/^SECRET_KEY = /c\SECRET_KEY = ${s_key}" \
    -e 's/DEBUG = True/DEBUG = False/' ${d_link}/${appname}/settings.py
    echo "[-] saved to: ${d_link}/${appname}/settings.py"

}

function do_debug(){
    echo '[+++] DEBUG on.'
    sed -i -e 's#db.sqlite3#debug.sqlite3#' \
    -e 's#DEBUG = False#DEBUG = True#'  ${d_link}/${appname}/settings.py
    cd ${d_link}
    do_ctl_uwsgi stop
    cp -av ${f_sqlite_src} debug.sqlite3
    ${py27} manage.py runserver 0.0.0.0:8000
}

function do_update_uwsgi(){
    echo '[+] setup uwsgi:'
    cd $(dirname $0)
    cp -fv ./uwsgi.ini /etc/uwsgi_${appname}.ini
    cp -fv ./init.d.uwsgi /etc/init.d/uwsgi_${appname} && chmod +x /etc/init.d/uwsgi_${appname}
    chkconfig --list |grep uwsgi |grep '3:on' || chkconfig uwsgi_${appname} on
    echo -e "You can try this: \n\tservice uwsgi_${appname} status"
}

function do_init(){
    do_update_uwsgi

    echo -e "\nnginx conf.d example: \n\t tools/nginx.conf.d.example"

    echo '[+] setup default secret_key:'
    create_secret_key
}

function do_require(){
    test -x /usr/local/bin/pip2.7 && exit || echo 'Where is pip2.7 on this host?'
    #yum -y install sqlite*
    #wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz && tar zxvf Python-2.7.13.tgz
    #cd Python-2.7.13 && ./configure && make && make install

    #wget https://pypi.python.org/packages/source/s/setuptools/setuptools-18.7.zip && unzip setuptools-18.7.zip
    #cd setuptools-18.7 && /usr/local/bin/python2.7 setup.py install

    #/usr/local/bin/easy_install-2.7 pip
    #/usr/local/bin/pip2.7 install -r requirements.txt
    #/usr/local/bin/pip2.7 install uwsgi

}

function do_collect(){
    echo '[+] do collectstatic'
    cd "${d_link}"
    ${py27} manage.py collectstatic --no-input
}

function do_test(){
    echo '[+] do test'
    cd "${d_link}"
    ${py27} manage.py test
}

function do_ctl_uwsgi(){
    echo "[+] do $1"
    service uwsgi_${appname} $1
}

function do_update(){
    echo "[+] deploy code:"
    mkdir -p ${d_target}
    rsync -av ${d_src}/ --exclude=".git/" ${d_target}/
    echo "[+] make symbol links:"
    rm -fv ${d_link}
    ln -sv ${d_target} ${d_link}
    ln -sv ${f_sqlite_src} ${f_sqlite_dest}
    update_django_settings
}

function do_cleanup(){
    # cleanup
    echo "[+] List dir:"
    ls -l ${d_root}
    echo "[-] File was last accessed n*24 hours ago:"
    find ${d_root} -maxdepth 1 -atime +7 -print |sort
    find ${d_root} -maxdepth 1 -atime +7 -delete;
    echo "[-] List dir again:"
    ls -l ${d_root}
}


function usage(){
    cat <<_EOF

USAGE:
    $0 init          :     init the env for uwsgi+nginx+django(with requirement as optional)
    $0 deploy        :     deploy the latest code(update,status,reload,cleanup)

    DON'T FORGET YOUR DB!
    [arguments as given below]

    collect          :     collectstatic
    cleanup          :     cleanup
    deploy           :     deploy from src to target
    init             :     init uwsgi
    reload           :     reload uwsgi
    restart          :     restart uwsgi
    stop             :     stop uwsgi
    status           :     status uwsgi
    test             :     test

    create_key       :     create secret_key
    update_setting   :     update django settings
    update_uwsgi     :     update uwsgi service control script and configuration

    require          :     python2.7, pip2.7, requirements.txt, uwsgi(pthon-devel), db
    d_src            :     ${d_src}
    d_root           :     ${d_root}
    d_link           :     ${d_link}

    debug            :     debug on
_EOF
}

case $1 in
    deploy)
        do_update
        #do_collect
        #do_test
        do_ctl_uwsgi status
        do_ctl_uwsgi reload
        do_ctl_uwsgi status
        do_cleanup
        ;;
    collect|cleanup|init|require|test|debug)
        do_$1
        ;;
    reload|restart|stop|status)
        do_ctl_uwsgi $1
        ;;
    create_key)
        create_secret_key
        ;;
    update_setting)
        update_django_settings
        ;;
    update_uwsgi)
        do_update_uwsgi
        ;;
    *)
        usage
        ;;
esac
