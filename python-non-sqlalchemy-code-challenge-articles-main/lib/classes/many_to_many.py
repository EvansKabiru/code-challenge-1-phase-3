class Article:
    # A class attribute to store all article instances.
    all = []

    def __init__(self, author, magazine, title):
        # Initializing the article with an author, magazine, and title.
        self.author = author
        self.magazine = magazine
        self.title = title
        # Adding the article to the list of all articles.
        Article.all.append(self)

    # Defining the title property for getting the article's title.
    @property
    def title(self):
        return self._title

    # Setter for the title with validation.
    @title.setter
    def title(self, new_title):
        # Title can't be changed after instantiation.
        if hasattr(self, '_title'):
            raise AttributeError('Title cannot be changed after the article is created.')
        # Title must be a string between 5 and 50 characters.
        if isinstance(new_title, str) and 5 <= len(new_title) <= 50:
            self._title = new_title
        else:
            raise ValueError('Title must be a string between 5 and 50 characters.')

    # Property for the author.
    @property
    def author(self):
        return self._author

    # Setter for author.
    @author.setter
    def author(self, new_author):
        # Author must be an instance of the Author class.
        if isinstance(new_author, Author):
            self._author = new_author
        else:
            raise TypeError('Author must be an instance of Author.')

    # Property for the magazine.
    @property
    def magazine(self):
        return self._magazine

    # Setter for the magazine.
    @magazine.setter
    def magazine(self, new_magazine):
        # Magazine must be an instance of the Magazine class.
        if isinstance(new_magazine, Magazine):
            self._magazine = new_magazine
        else:
            raise TypeError('Magazine must be an instance of Magazine.')


class Author:
    def __init__(self, name):
        # Initializing the author with a name.
        self.name = name

    # Property for the author's name.
    @property
    def name(self):
        return self._name

    # Setter for name with validation.
    @name.setter
    def name(self, new_name):
        # Name can't be changed once it's set.
        if hasattr(self, '_name'):
            raise AttributeError('Name cannot be changed after instantiation.')
        # Name must be a string and non-empty.
        if isinstance(new_name, str) and len(new_name) > 0:
            self._name = new_name
        else:
            raise ValueError('Name must be a non-empty string.')

    # Method to return all articles written by the author.
    def articles(self):
        return [article for article in Article.all if article.author == self]

    # Method to return all unique magazines the author has contributed to.
    def magazines(self):
        return list({article.magazine for article in self.articles()})

    # Method to add a new article written by the author.
    def add_article(self, magazine, title):
        # Create a new Article instance and associate it with this author.
        return Article(self, magazine, title)

    # Method to return all unique topic areas (categories of magazines) the author has contributed to.
    def topic_areas(self):
        areas = list({magazine.category for magazine in self.magazines()})
        return areas if areas else None


class Magazine:
    # Class attribute to store all magazine instances.
    all = []

    def __init__(self, name, category):
        # Initializing the magazine with a name and a category.
        self.name = name
        self.category = category
        # Adding the magazine to the list of all magazines.
        Magazine.all.append(self)

    # Property for the magazine's name.
    @property
    def name(self):
        return self._name

    # Setter for the magazine's name with validation.
    @name.setter
    def name(self, new_name):
        # Name must be between 2 and 16 characters.
        if isinstance(new_name, str) and 2 <= len(new_name) <= 16:
            self._name = new_name
        else:
            raise ValueError('Name must be a string between 2 and 16 characters.')

    # Property for the magazine's category.
    @property
    def category(self):
        return self._category

    # Setter for category with validation.
    @category.setter
    def category(self, new_category):
        # Category must be a non-empty string.
        if isinstance(new_category, str) and len(new_category) > 0:
            self._category = new_category
        else:
            raise ValueError('Category must be a non-empty string.')

    # Method to return all articles published by the magazine.
    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    # Method to return all unique authors who have written for this magazine.
    def contributors(self):
        return list({article.author for article in self.articles()})

    # Method to return a list of article titles published in this magazine.
    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    # Method to return a list of authors who have written more than 2 articles for this magazine.
    def contributing_authors(self):
        author_counts = {}
        for article in self.articles():
            author_counts[article.author] = author_counts.get(article.author, 0) + 1
        # Return authors who have more than 2 articles published in this magazine.
        return [author for author, count in author_counts.items() if count > 2] or None

    @classmethod
    def top_publisher(cls):
        # Class method to return the magazine with the most articles published.
        if not Article.all:
            return None
        # Count the number of articles per magazine.
        article_count = {}
        for article in Article.all:
            article_count[article.magazine] = article_count.get(article.magazine, 0) + 1
        # Find the magazine with the maximum number of articles.
        max_count = max(article_count.values())
        top_magazines = [magazine for magazine, count in article_count.items() if count == max_count]
        return top_magazines[0] if top_magazines else None


if __name__ == "__main__":
    # Step 1: Create some Authors and Magazines
    author1 = Author("Jane Doe")
    author2 = Author("John Smith")

    magazine1 = Magazine("Tech Monthly", "Technology")
    magazine2 = Magazine("Science Today", "Science")
    magazine3 = Magazine("Art Weekly", "Art")

    # Step 2: Add Articles to the Authors
    article1 = author1.add_article(magazine1, "The Future of AI")
    article2 = author1.add_article(magazine2, "Exploring Quantum Physics")
    article3 = author2.add_article(magazine1, "Blockchain in Finance")
    article4 = author2.add_article(magazine3, "Modern Art Movements")

    # Step 3: Print information about articles, authors, and magazines

    # Print all articles written by author1
    print(f"Articles by {author1.name}:")
    for article in author1.articles():
        print(f"- {article.title} in {article.magazine.name}")

    # Print all unique magazines the author1 has contributed to
    print(f"\nMagazines contributed to by {author1.name}:")
    for mag in author1.magazines():
        print(f"- {mag.name} ({mag.category})")

    # Print all topic areas for author1 (magazine categories they have contributed to)
    print(f"\nTopic areas for {author1.name}:")
    print(author1.topic_areas())

    # Print all authors who have written for magazine1
    print(f"\nAuthors who have written for {magazine1.name}:")
    for author in magazine1.contributors():
        print(f"- {author.name}")

    # Print all article titles in magazine1
    print(f"\nArticles in {magazine1.name}:")
    for title in magazine1.article_titles():
        print(f"- {title}")

    # Print contributing authors to magazine1
    print(f"\nContributing authors to {magazine1.name} (more than 2 articles):")
    contributing_authors = magazine1.contributing_authors()
    if contributing_authors:
        for author in contributing_authors:
            print(f"- {author.name}")
    else:
        print("No contributing authors with more than 2 articles.")

    # Step 4: Print the top publisher (the magazine with the most articles)
    top_magazine = Magazine.top_publisher()
    if top_magazine:
        print(f"\nTop publisher (most articles): {top_magazine.name}")
    else:
        print("\nNo top publisher, no articles available.")
