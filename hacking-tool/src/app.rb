require 'sinatra'
require 'sinatra/reloader' if development?
require './tool'

set :port, ENV['PORT'] if ENV['PORT']

def humanize(text)
  text.to_s.downcase.tr('_', ' ').capitalize
end

get '/' do
  erb :index
end

post '/' do
  @method = params.fetch(:method, '')
  @message = params.fetch(:message, '')

  if @method.include?('exec') || @message.include?('exec')
    halt 'Hacker detected!'
  end

  unless @method.strip.empty?
    begin
      @result = Tool.send(@method, @message).to_s
      logger.info "@method #{@method}, @message #{@message}"
      logger.info "@result #{@result}"
    rescue NoMethodError => e
      @error = e.message
    rescue StandardError => e
      logger.info "Error: #{e.message}"
    end
  end
  erb :index
end

__END__

@@ layout
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title></title>
    <style>
      body {
        font-family: sans-serif;
        margin: 0;
        color: #282c37;
        background: #d9e1e8;
      }
      header {
        background: #2b90d9;
        overflow: auto;
      }
      .container {
        display: block;
        width: 600px;
        margin: 0 auto;
      }
      .logo {
        float: left;
        font-size: 2em;
        color: #282c37;
        text-decoration: none;
        padding: 16px 8px;
      }
      textarea {
        font-family: monospace;
        resize: none;
        padding: 1px;
        margin: 16px 0;
        width: 100%;
        background: white;
        min-height: 100px;
        border: 1px solid #9baec8;
      }
      hr {
        margin: 16px 0;
      }
      .paragraph {
        margin-top: 16px;
        font-weight: 200;
      }
      .error {
        color: #E71D36;
        width: 100%;
      }
    </style>
  </head>
  <body>
    <header>
      <div  class="container">
        <a class="logo" href="#">
          Hacking Tool 🛠
        </a>
      </div>
    </header>
    <main class="container">
      <%= yield %>
    </main>
  </body>
</html>

@@ index
<div class="paragraph">
  This is my custom hacking tool, very useful during CTFs 🚩!
</div>
<form action="/" method="POST">
  <textarea autofocus name="message"><%= @message %></textarea>
  <!-- <input type="text" name="option"/> -->
  <br>
  <select name="method">
    <% Tool.exposed_methods.each do |method| %>
      <option value="<%= method %>"><%= humanize(method) %></option>
    <% end %>
  </select>
  <input type="submit">
  <hr/>
  <textarea><%= @result %></textarea>
  <% if @error %>
    <!-- <div class="error"><%= @error %></div> -->
  <% end %>
</form>
