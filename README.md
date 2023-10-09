# fastapi-test
I wanted to be able to pull out the variables directly from the route string... probably top 5 
hackiest things I've done 
in python...

but it works? 

I haven't tested this on very many cases at all, obviously I only wrote a function for get, but presumably
you could also write one for the other standard http methods. Get's are the easiest because you don't 'often' do much
deserializing from a git body itself. 
