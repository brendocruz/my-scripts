cd src/parsers
for FILENAME in $(ls .)
do
	chmod +x ${FILENAME}
	ln --relative -s ${FILENAME} /usr/bin/my-${FILENAME}
done
