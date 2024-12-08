class Article:
    all = []  #Class variable to hold all articles
    
    def __init__(self, author, magazine, title):
        # Validate input types and constraints
        if not isinstance(author, Author):
            raise ValueError("Author must be an Author instance.")
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be a Magazine instance.")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        self.author = author
        self.magazine = magazine
        self.__setattr__('_title', title)  # Bypass setattr restrictions during initialization
        author._articles.append(self)
        magazine._articles.append(self)
        # Append the created article to the 'all' list
        Article.all.append(self)
        # Add the article to the magazine's list of articles
        magazine.add_article(self)

    def __setattr__(self, key, value):
        # Prevent changes to the 'title' attribute after instantiation
        if key == "_title" and hasattr(self, '_title'):
            raise AttributeError("Cannot modify the title of an Article after instantiation.")
        super().__setattr__(key, value)

    @property
    def title(self):
        # Provide read-only access to the 'title' attribute
        return self._title

        
class Author:
    def __init__(self, name):
        # Validate that name is a non-empty string
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string.")
        self.__setattr__('_name', name)  # Bypass setattr restrictions during initialization
        self._articles = []

    def __setattr__(self, key, value):
        # Prevent changes to the 'name' attribute after instantiation
        if key == "_name" and hasattr(self, '_name'):
            raise AttributeError("Cannot modify the name of an Author after instantiation.")
        super().__setattr__(key, value)

    @property
    def name(self):
        # Provide read-only access to the 'name' attribute
        return self._name

    def articles(self):
        # Returns a list of all articles written by the author
        return self._articles

    def magazines(self):
        # Returns a unique list of magazines the author has contributed to
        return list(set(article.magazine for article in self._articles))

    def add_article(self, magazine, title):
        # Creates a new article and associates it with this author and the given magazine
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be a Magazine instance.")
        article = Article(self, magazine, title)
        self._articles.append(article)
        magazine._articles.append(article)
        return article
    def articles(self):
        # Ensures the list contains only unique articles
        return list(set(self._articles))

    def topic_areas(self):
        # Returns unique categories of magazines the author has contributed to
        return list(set(magazine.category for magazine in self.magazines())) if self._articles else None


class Magazine:
    _all = []

    def __init__(self, name, category):
        # Validate that name and category are appropriate
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
        self.name = name
        self.category = category
        
        @property
        def name(self):
            return self._name
        
        @name.setter
        def name(self, value):
            if not (2 <= len(value) <=16):
                raise ValueError("Magazine name must be between 2 and 16 characters")
            self._name = value
            
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if len(value) == 0:
            raise ValueError("Category cannot be empty.")
        self._category = value    
        
        self._articles = []
        Magazine._all.append(self)

    def articles(self):
        # Returns only unique characters
        return list(set(self._articles))
    
    def add_article(self, article):
        if article not in self._articles:
            self._articles.append(article) 
            
    def contributors(self):
        # Returns a unique list of authors who have written for this magazine
        return list(set(article.author for article in self._articles))

    def article_titles(self):
        # Returns the titles of all articles in this magazine
        return [article.title for article in self._articles] if self._articles else None

    def contributing_authors(self):
        # Returns authors with more than 2 articles in this magazine
        author_count = {author: 0 for author in self.contributors()}
        for article in self._articles:
            author_count[article.author] += 1
        result = [author for author, count in author_count.items() if count > 2]
        return result if result else None

    @classmethod
    def top_publisher(cls):
        # Returns the magazine with the most articles
        return max(cls._all, key=lambda magazine: len(magazine._articles), default=None)
