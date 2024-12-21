import rsa 

(public, private) = rsa.newkeys(512)
(public2, private2) = rsa.newkeys(512)

print(f"privat key {private} \n")
print(f"public key {public} \n")

message = "Hello world".encode('utf8')
message_encrypt = rsa.encrypt(message, public)

message_delivired = rsa.decrypt(message_encrypt, private)
print(f"decode message: {message_delivired.decode('utf-8')}")

message_delivired = rsa.decrypt(message_encrypt, private2)
print(f"decode message: {message_delivired.decode('utf-8')}")