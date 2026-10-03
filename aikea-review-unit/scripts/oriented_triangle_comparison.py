"""Scope: Prove a bijection of oriented triangle surfaces within the declared export tolerance."""
from itertools import product
import numpy as np


class OrientedTriangleComparison:
    def __init__(self, tolerance=0.000002):
        self.tolerance = tolerance

    def compare(self, key, before, after):
        original, exported = before[0][before[1]], after[0][after[1]]
        if len(original) != len(exported):
            raise ValueError(f'{key}: triangle count changed')
        neighbours, errors = self.candidates(original, exported)
        matched = self.match(neighbours)
        if len(matched) != len(original):
            raise ValueError(f'{key}: no complete oriented triangle correspondence')
        distance = max(errors[source,target] for target,source in matched.items())
        return {'part':key, 'triangles':len(original), 'maximum_vertex_error_mm':distance*1000}

    def candidates(self, original, exported):
        buckets = {}
        for index, center in enumerate(exported.mean(axis=1)):
            buckets.setdefault(tuple(np.floor(center/self.tolerance).astype(int)), []).append(index)
        neighbours, errors = [], {}
        for index, triangle in enumerate(original):
            cell = np.floor(triangle.mean(axis=0)/self.tolerance).astype(int)
            nearby = [other for delta in product((-1,0,1),repeat=3)
                      for other in buckets.get(tuple(cell+delta), [])]
            candidates = []
            for other in nearby:
                # Cyclic permutations preserve winding; reversing an oriented face does not pass.
                error = min(np.linalg.norm(triangle-np.roll(exported[other], shift, axis=0), axis=1).max()
                            for shift in range(3))
                if error < self.tolerance:
                    candidates.append(other)
                    errors[index,other] = float(error)
            neighbours.append(candidates)
        return neighbours, errors

    def match(self, neighbours):
        matched, reverse = {}, {}
        for start in range(len(neighbours)):
            queue, seen, parents, end = [start], set(), {}, None
            for source in queue:
                for target in neighbours[source]:
                    if target in seen:
                        continue
                    seen.add(target)
                    parents[target] = source
                    if target not in matched:
                        end = target
                        break
                    queue.append(matched[target])
                if end is not None:
                    break
            if end is None:
                continue
            while end is not None:
                source = parents[end]
                previous = reverse.get(source)
                matched[end] = source
                reverse[source] = end
                end = previous
        return matched
