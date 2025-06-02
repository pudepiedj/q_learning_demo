'''
About as simple a class as you can get
This isn't really true, is it?
'''

class ReallySimpleClass:

    """This class is called 'ReallySimple Class'."""

    name = "Really Simple Class"

    i = 123445

class MoreComplicatedClassButNotMuch:

    """This class is called 'MoreComplicatedClassButNotMuch'."""
    
    def __init__(self, *args, **kwargs):

        self.feedback = "Gives as good as it gets"

def main():

    first = ReallySimpleClass()
    second = ReallySimpleClass()

    print(first)

    print(first.__dict__)
        
    print(first.name)
    print(first.i)
    print(first.__doc__)

    print(second)
    print(second.name)
    print(second.i)
    print(second.__doc__)

    print(__doc__)
          
    feed_in = MoreComplicatedClassButNotMuch()

    print(feed_in,'\n')
    print(feed_in.feedback,'\n')
    print(feed_in.__doc__,'\n')
    print(feed_in, __doc__,'\n')
    print(feed_in,'\n')
    print(MoreComplicatedClassButNotMuch().feedback,'\n')


if __name__ == "__main__":
    main()
