import rsa 

(public, privat) = rsa.newkeys(512)

print(f"privat key {privat} \n")
print(f"public key {public} \n")

message = "Hello world".encode('utf8')
message_encrypt = rsa.encrypt(message, public)

message_delivired = rsa.decrypt(message_encrypt, privat)
print(f"decode message: {message.decode('utf-8')}")