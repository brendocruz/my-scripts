cd src/parsers
for FILENAME in $(ls .)
do
	rm /usr/bin/my-${FILENAME}
done
