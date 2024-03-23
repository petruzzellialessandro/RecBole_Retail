import numpy as np

class RecRetailMetrics:
    def __init__(self, predicted_items, ground_truth, users, config, total_items, item_popularity):
        self.predicted_items = np.array(predicted_items)
        self.ground_truth = np.array(ground_truth)
        self.config = config
        self.users = users if type(users) == np.ndarray else np.array(users)
        self.top_k = config["topk"] if "topk" in config else [5, 10, 20, 50, 100]
        self.tail_length = config["tail_length"] if "tail_length" in config else 0.2
        self.item_popularity = item_popularity
        self.tail_items = self._set_tail_items()
        self.total_items = total_items

    def _set_tail_items(self):
        sorted_items_by_popularity = sorted(self.item_popularity.items(), key=lambda x: x[1])
        return [item[0] for item in sorted_items_by_popularity[:int(len(sorted_items_by_popularity) * self.tail_length)]]

    def compute_metric_per_k(self, metric_func):
        results = {}
        for k in self.top_k:
            result = metric_func(k)
            results[f"{metric_func.__name__}@{k}"] = result
        return results
    
    def precision(self, k):
        hits_at_k = [np.isin(pred[:k], gt).sum() for pred, gt in zip(self.predicted_items, self.ground_truth)]
        precision_at_k = np.mean([hits / min(k, len(pred)) for hits, pred in zip(hits_at_k, self.predicted_items)])
        return precision_at_k

    def hit(self, k):
        hit_rate_at_k = np.mean([np.any(np.isin(pred[:k], gt)) for pred, gt in zip(self.predicted_items, self.ground_truth)])
        return hit_rate_at_k

    def recall(self, k):
        recall = np.isin(self.predicted_items[:, :k], self.ground_truth).sum() / len(self.users)
        return recall

    def mean_reciprocal_rank(self, k):
        reciprocal_ranks = []
        for pred, true in zip(self.predicted_items, self.ground_truth):
            idx = np.where(np.isin(pred[:k], true))[0]
            if len(idx) > 0:
                reciprocal_ranks.append(1.0 / (idx[0] + 1))
            else:
                reciprocal_ranks.append(0)
        return np.mean(reciprocal_ranks)

    def average_popularity(self, k):
        user_popularities = []
        for user_index in range(len(self.users)):
            user_items = self.predicted_items[user_index, :k]
            user_popularity = np.mean([self.item_popularity.get(item, 0) for item in user_items if item in self.item_popularity])
            user_popularities.append(user_popularity)

        avg_popularity = np.mean(user_popularities) if user_popularities else 0
        return avg_popularity

    def tail_percentage(self, k):
        user_tail_percentages = []
        for user_index in range(len(self.users)):
            user_items = self.predicted_items[user_index, :k]
            user_tail_percentage = np.mean([1 if item in self.tail_items else 0 for item in user_items])
            user_tail_percentages.append(user_tail_percentage)
        return np.mean(user_tail_percentages)

    def item_coverage(self, k):
        unique_predicted = np.unique(np.concatenate(self.predicted_items[:, :k]))
        coverage = len(unique_predicted) / self.total_items
        return coverage

    def compute_all_metrics(self):
        metrics = {}

        recall_results = self.compute_metric_per_k(self.recall)
        metrics.update(recall_results)

        precision_results = self.compute_metric_per_k(self.precision)
        metrics.update(precision_results)

        hit_rate_results = self.compute_metric_per_k(self.hit)
        metrics.update(hit_rate_results)

        mrr_results = self.compute_metric_per_k(self.mean_reciprocal_rank)
        metrics.update(mrr_results)

        coverage_results = self.compute_metric_per_k(self.item_coverage)
        metrics.update(coverage_results)
        
        avg_popularity_results = self.compute_metric_per_k(self.average_popularity)
        metrics.update(avg_popularity_results)

        tail_percentage = self.compute_metric_per_k(self.tail_percentage)  
        metrics.update(tail_percentage)

        
        return metrics


