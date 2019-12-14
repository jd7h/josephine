# Thoughts on database design

Thoughts on database design for Josephine
Borrowed from Hans de Zwart's booklist and GoodReads. :)

## Book

```
Book:
mandatory information:
title: char[255] 
author: char[255]
```
For the title, char[255] seems like a safe option. The longest title in my goodreads library (1000+ titles) is 162 characters. The Guinness Book of Records lists 11,000+ chars as the longest title ever, but that seems overkill?

For authors: Do we want Author objects or just the name as a string? If we include information about gender, nationality, etc, in an Author object we could generate cool "reading bias" statistics >:) (can we get this via GoodReads?). Filing this as a nice-to-have for now.

```
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

ISBN (from [wikipedia](https://en.wikipedia.org/wiki/International_Standard_Book_Number):
"An ISBN is assigned to each separate edition and variation (except reprintings) of a publication. For example, an e-book, a paperback and a hardcover edition of the same book will each have a different ISBN. The ISBN is ten digits long if assigned before 2007, and thirteen digits long if assigned on or after 1 January 2007."

## Shelf

Or: category, tag, booklist, ...
Going with Shelf because that's the name in my head, courtesy of GR. ;)
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
