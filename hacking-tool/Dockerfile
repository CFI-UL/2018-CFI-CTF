FROM ruby:2.5

WORKDIR /usr/src/app

COPY ./src/Gemfile .
COPY ./src/Gemfile.lock .
RUN bundle install

COPY ./src .

CMD [ "ruby", "./app.rb" ]
