# Thoughts on database design

Thoughts on database design for Josephine
Borrowed from Hans de Zwart's booklist and GoodReads. :)

## Book

```
Book:
mandatory information:
title: char[255] seems like a safe option. The longest title in my goodreads library (1000+ titles) is 162 character. The guiness book of records lists 11,000+ chars as the longest title ever, but that seems overkill?
author: list of Author objects? or just full names as strings char[255] and that's it? If we include information about gender, nationality, etc, in an Author object we could generate cool "reading bias" statistics >:) (can we get this via GoodReads?)

optional fields:
language: is there a standard way to encode languages?
num_pages: integer
publisher:
binding:
date_pub: 
ISBN10: 
ISBN13: 
```

What do we do with editions? What if two users have read the same title but different editions? Are updates about a particular edition? Maybe add a 'default' edition? 

## Shelf
```
Shelf:
name: char[255]
```

## Status

To read, currently reading, read -- also known as 'unique shelves' or 'exclusive shelves' on GR

```
Status
name: char[255]
```

## Changes to book Status

```
StatusUpdate:
book: models.ForeignKey(Book)
change_date: date
new_status: models.ForeignKey(Status)
if multiuser: user: models.ForeignKey(User) ofzo?
```

## Changes to book categories/tags

```
ShelfUpdate:
book: models.ForeignKey(Book)
change_date: date
shelf: models.ForeignKey(Shelf)
if multiuser: user: models.ForeignKey(User) ofzo?
```
