pyc:
	find . -name \*.pyc -delete

flush:
	echo "flush_all" | nc -w 2 localhost 11211

restart:
	sudo systemctl restart gunicorn
	sudo systemctl restart nginx
	sudo systemctl restart memcached
