import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical

# 定数定義
MOVES = {0: "グー", 1: "チョキ", 2: "パー", 3: "王様", 4: "農民"}
NUM_CLASSES = 5
SEQ_LENGTH = 5

# 勝敗ルール (KeyがValueに勝つ)
WIN_RULES = {0: [1, 4], 1: [2, 4], 2: [0, 4], 3: [0, 1, 2], 4: [3]}

# カウンター戦略の候補リスト (Key(予測)に対して出す手の候補)
COUNTER_STRATEGIES = {
    0: [2, 3],
    1: [0, 3],
    2: [1, 3],
    3: [4],
    4: [0, 1, 2],
}


class JankenAI:
    def __init__(self):
        self.model = self._build_model()
        self.history = []  # ユーザーの手の履歴

    def _build_model(self):
        """LSTMモデルの構築"""
        model = Sequential(
            [
                LSTM(32, input_shape=(SEQ_LENGTH, NUM_CLASSES), unroll=True),
                Dense(NUM_CLASSES, activation="softmax"),
            ]
        )
        model.compile(
            loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
        )
        return model

    def predict_next_move(self):
        """履歴からユーザーの次の手を予測する"""
        if len(self.history) < SEQ_LENGTH:
            # データ不足時はランダムな確率分布を返す
            return np.full(NUM_CLASSES, 1 / NUM_CLASSES)

        last_seq = self.history[-SEQ_LENGTH:]
        last_seq_one_hot = to_categorical(last_seq, num_classes=NUM_CLASSES)
        input_data = np.expand_dims(last_seq_one_hot, axis=0)

        # 確率分布を取得 (例: [0.1, 0.8, 0.05, 0.05, 0.0])
        pred_probs = self.model.predict(input_data, verbose=0)[0]
        return pred_probs

    def get_counter_move(self, pred_probs):
        """予測確率が最も高い手に対するカウンターを選ぶ"""
        if len(self.history) < SEQ_LENGTH:
            return np.random.randint(0, NUM_CLASSES)

        predicted_user_move = int(np.argmax(pred_probs))
        candidates = COUNTER_STRATEGIES[predicted_user_move]
        return np.random.choice(candidates)

    def update_and_train(self, user_move):
        """履歴を更新し、オンライン学習を行う"""
        self.history.append(user_move)

        # データが溜まったら学習 (直近のパターンを即座に反映)
        if len(self.history) > SEQ_LENGTH:
            X_train, y_train = self._prepare_data()
            # 3エポック学習 (オンライン学習)
            self.model.fit(X_train, y_train, epochs=3, batch_size=1, verbose=0)

    def _prepare_data(self):
        """履歴から学習データを作成"""
        X, y = [], []
        # 全履歴を使って再学習（忘却を防ぐため）
        for i in range(len(self.history) - SEQ_LENGTH):
            seq_in = self.history[i : i + SEQ_LENGTH]
            seq_out = self.history[i + SEQ_LENGTH]
            X.append(to_categorical(seq_in, num_classes=NUM_CLASSES))
            y.append(to_categorical(seq_out, num_classes=NUM_CLASSES))
        return np.array(X), np.array(y)

    def determine_result(self, user_move, ai_move):
        """勝敗判定"""
        if user_move == ai_move:
            return "あいこ"
        if user_move in WIN_RULES[ai_move]:
            return "AIの勝ち"
        return "あなたの勝ち"


# シングルトンインスタンスを作成（簡易的な状態保持）
ai_instance = JankenAI()
