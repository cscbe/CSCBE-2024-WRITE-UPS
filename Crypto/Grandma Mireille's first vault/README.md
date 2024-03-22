# CHALLENGE_TITLE
Grandma Mireilles first vault

## Category
Cryptography

## Estimated difficulty
Medium

## Description
This challenge is about recreating a PEM private key wile parts of it are obscured (https://blog.cryptohack.org/twitter-secrets)

## Scenario
My grandma was always a fan of using paper instead of storing items on a harddrive. Paper is of course a very secure method to store your secrets and private keys, but it also has it downsides.
One of those downsides lies in the fact that she forgot to laminate the paper, which created a bit of a problem when she spilled coffee all over her pile of secret keys.
She thought that she ruined all of the paper and that she never would be able to retrieve the secrets she noted down in her encrypted file, but I know it is still technically possible by using some clever tricks.
Can you help her retrieve her private key and decrypt her files ?

## Write-up
Follow the steps as explained in the following url:https://blog.cryptohack.org/twitter-secrets 
Then use the private key to decrypt the txt with the following command:
openssl rsautl -decrypt -inkey private_key.pem -in <encrypted file> -out <decrypted file>


## Flag
CSC{Not-Only_Hubert_had-a_vault_collection}

## Creator
Sander Van Dessel

## Creator bio
[Hi, I am Sander Van Dessel and I am a security consultant at NVISO. I love to do CTFS and play D&D (No I don't dress up as a dwarf and throw bean bags at people while shouting fireball). I also seem to have discoverd a passion for grandparent challenges.]

[- https://www.linkedin.com/in/sander-van-dessel-622aba144/]