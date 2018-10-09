FROM httpd:latest
COPY httpd.conf /usr/local/apache2/conf
COPY challenge_files/print_flag /print_flag
RUN chown root /print_flag
RUN chmod 111 /print_flag
