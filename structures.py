"""
scraper.structures
~~~~~~~~~~~~~~~~~~~
Data structures that power scraper.
"""
from typing import List, Callable


class Batch:
    def __init__(self, start_index: int, end_index: int, items: List):
        self.start_index = start_index
        self.end_index = end_index
        self.items = items

class BatchList:
    def __init__(self, batch_size: int, callback: Callable[[Batch], None]):
        """A data structure that contains a list of items. When the list
        exceeds the batch size given, the callback is called with the current
        batch as an argument.
        Example:
        >>> batch_list = BatchList(batch_size=2, callback=lambda batch: print(batch.items))
        >>> batch_list.add(1)
        >>> batch_list.add(2)  # batch_size reached, callback called.
        [1, 2]
        >>> batch_list.add(3)
        >>> batch_list.add(4)  # batch_size reached, callback called.
        [3, 4]
        Args:
            batch_size (int): After how many inserted items should the callback
                be called.
            callback (Callable[[Batch], None]): Continually called each time
                the batch_size is reached.
        """
        self._batch_size = batch_size
        self._callback = callback

        self._items: List = []
        self._batch_number = 0

    @property
    def items(self):
        """Called when retrieving items by property.
        Returns:
            List[any]: Any item type.
        """
        return self._items

    @items.setter
    def items(self, items):
        """Prevent items to be set directly by property.
        """
        raise ValueError('Not allowed to modify items manually, only add items'
                         'via the add(item) method.')

    def add(self, item) -> None:
        """Add an item to the BatchList.
        Args:
            item (any): Any item type.
        Returns:
            None
        """
        self._items.append(item)
        if self._should_call():
            self._callback(self.get_current_batch())
            self._batch_number += 1

    def get_current_batch(self) -> Batch:
        """Returns the current batch, based on _batch_number.
        Returns:
            Batch: A Batch object.
        """
        start_index = self._batch_number * self._batch_size
        return Batch(
            start_index=start_index,
            end_index=len(self._items),
            items=self._items[start_index:]
        )

    def _should_call(self) -> bool:
        """Whether _callback should be called.
        Returns:
            bool: Whether _callback should be called.
        """
        if len(self._items) == 1:
            return False
        return len(self._items) % self._batch_size == 0