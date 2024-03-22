# CHALLENGE_TITLE
Grandma Mireille's final vault

## Category
Cryptography

## Estimated difficulty
Hard

## Description
The challenge gives the participants 20 rings and 2 images with Tengwar (Elvish) and Kuzdul (dwarvish) from Tolkiens LOTR.
They will have to translate both languages (elvish is just translating to english by translating each letter, dwarvish however will be harder because thet first have to tran
slate the characters and then look up the dwarvish words and translate them).
Those 2 hint to the fact that they will have to use the 7 dwarven rings and Shamir's secret sharing.
They have to look at the metadata (the metadata is non hidden or obfuscated) to find the hashes used in the shamir secret sharing.

Fun fact: I will include other hashes called rings in my other challenges that they will also be able to use (I created 20 parts and at least 7 are needed)

## Scenario
Grandma Mireille loves to read books, not a month goes by when she does not have a new pile of books laying somewhere in her loving room.
While most of them are non-fiction, she sometimes is open to read fiction as well.
One of these rare occasions involved the works of Tolkien. She mainly started to read them because she is also very interested in languages (She often joined "Het Groot Dictee der Nederlandse Taal" and often had almost no mistakes),
and Tolkien is of course also a well known linguist who created multiple languages for his novels.
When I was recently searching for a clue of her second vault, I found some notes written in a strange language, accompanied by 20 beatifull rings.
Might these contain a hint to open her second vault ?

## Write-up
The first step is to solve the Tengwar and Kuzdul languages, you can easely find an explenation online (e.g.https://www.pinterest.com/pin/5136987055067080/ for tengwar and https://www.pinterest.com/pin/845269423795862333/ for Kuzdul). The kuzdul however will not translate to English by just decyphering the characters, you have to actually look up the words in a dictionary (https://thedwarrowscholar.com/khuzdul/documents-dictionaries/). The tengwar sentence translates to: Seek help from Shamir the wise. The kuzdul translates to: Seven secrets (Oroc.) to give (presents) grandmother dwarf to them (masculine/neuter). Because kuzduk uses other gramatic rules you have to change the sentence to make more sence in english: Seven secrets were given to the dwarven grandmothers.
By using these hints, you know know that u will need to use Shamir and that it has something to do with the seven dwarven rings.
The set of 7 rings all have a hash in their metadata in the camera maker field.
By entering these seven hashes (the order does not matter) in a shamir decryptor (e.g. https://iancoleman.io/shamir/ or https://www.geeksforgeeks.org/shamirs-secret-sharing-algorithm-cryptography/) you will obtain the flag: CSC{0ne_gr4ndma_2_rul3_th3m_4ll}

## Flag
CSC{0ne_gr4ndma_2_rul3_th3m_4ll}

## Creator
Sander Van Dessel

## Creator bio
[Hi, I am Sander Van Dessel and I am a security consultant at NVISO. I love to do CTFS and play D&D (No I don't dress up as a dwarf and throw bean bags at people while shouting fireball). I also seem to have discoverd a passion for grandparent challenges.]

[- https://www.linkedin.com/in/sander-van-dessel-622aba144/]
