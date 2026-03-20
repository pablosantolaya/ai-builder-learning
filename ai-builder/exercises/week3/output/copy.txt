class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.word_count = len(content.split())

    def summarize(self):
        return self.content[:100] + "..."
    
    def info(self):
        return f"Document: {self.title} ({self.word_count} words)"


doc1 = Document("Q3 Report", "Revenue increased by 15% in the third quarter due to strong sales performance across all regions and improved operational efficiency in the supply chain management department")
doc2 = Document("Meeting Notes", "Discussed the project timeline and budget allocation for next quarter")

print(doc1.summarize())
print(doc2.summarize())

print(doc1.info())
print(doc2.info())

print(doc1.word_count)
print(doc2.word_count)