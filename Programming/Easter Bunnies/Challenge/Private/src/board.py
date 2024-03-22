import random


class Board:
    def __init__(self, amount_boxes):
        self.amount_boxes = amount_boxes
        self.boxes_dict = None
        self.chains = None
        self.max_chain = amount_boxes
        while self.max_chain > amount_boxes // 2:
            self.init_boxes()

    def init_boxes(self):
        labels = [i for i in range(1, self.amount_boxes + 1)]
        contents = [i for i in range(1, self.amount_boxes + 1)]
        random.shuffle(contents)
        self.chains = self.find_chains(labels, contents)
        self.calculate_boxes_dict()

    def shuffle_eggs(self):
        for (_, contents) in self.chains:
            random.shuffle(contents)
        self.calculate_boxes_dict()

    def calculate_boxes_dict(self):
        self.boxes_dict = dict()
        for (labels, contents) in self.chains:
            for label, content in zip(labels, contents):
                self.boxes_dict[label] = content

    def find_chains(self, labels, contents):
        seen = set()
        items = {label: content for label, content in zip(labels, contents)}
        chains = []
        for label in labels:
            if label not in seen:
                start = label
                current = label
                seen.add(current)

                chain_labels = [current]
                chain_contents = [items[current]]

                while items[current] != start:
                    current = items[current]
                    seen.add(current)

                    chain_labels.append(current)
                    chain_contents.append(items[current])
                chains.append((chain_labels, chain_contents))
        self.max_chain = max(len(labels) for (labels, _) in chains)
        return chains

    def get_box_contents(self, label):
        if 0 < label <= self.amount_boxes:
            return self.boxes_dict[label]

    def __str__(self):
        return str(self.boxes_dict)


if __name__ == '__main__':
    b = Board(1000)
    print(b)
    print(b.chains)
    print(b.max_chain)
    b.shuffle_eggs()
    print(b)
    print(b.chains)
    print(b.max_chain)
