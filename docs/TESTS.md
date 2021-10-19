models
=======

shelf

you may not have 2 shelves or statuses with the same name

status

you may not have 2 shelves or statuses with the same name

book

a book always has a status
a book always has a title
a book always has an author
star rating is always between 1 and 5 (discreet)
1 star leads to "1 star" string and not to "1 stars".
if a status is deleted, all books with that status will be reset to the default status.
an isbn10 has exactly 10 characters
an isbn13 has exactly 13 characters
a book has either no pagecount or a positive pagecount
a read date is never in the future
a book always has exactly 1 status

update

a status update is never in the future

readinggoal

there is only 1 reading goal per year
a reading goal is always positive

site preferences

there is only 1 site preference object per user

views
======

All views
if the user is authenticated, the menu says 'welcome, username'

Single
If the user is authenticated, the user can update the rating of a book
If the user is not logged in, the user cannot update the 'rate this book' module
