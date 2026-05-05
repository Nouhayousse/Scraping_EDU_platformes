import json


class CourseraPipeline:

    def open_spider(self, spider):
        self.file = open("courses.json", "w", encoding="utf-8")
        self.data = []

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item

    def close_spider(self, spider):
        json.dump(self.data, self.file, ensure_ascii=False, indent=4)
        self.file.close()