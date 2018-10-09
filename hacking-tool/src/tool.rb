require 'base64'

class Tool  
  def self.decode_base64(message)
    Base64.decode64(message)
  end

  def self.encode_base64(message)
    Base64.encode64(message)
  end

  def self.encode_hexadecimal(message)
    message.unpack('H*')[0]
  end

  def self.decode_hexadecimal(message)
    [message].pack('H*')
  end

  def self.md5(message)
    Digest::MD5.hexdigest(message)
  end

  def self.sha1(message)
    Digest::SHA1.hexdigest(message)
  end

  def self.sha2(message)
    Digest::SHA2.hexdigest(message)
  end

  def self.exposed_methods
    %i[
      encode_base64
      decode_base64
      encode_hexadecimal
      decode_hexadecimal
      md5
      sha1
      sha2
    ]
  end
end
