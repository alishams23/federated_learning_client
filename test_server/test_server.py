import flwr as fl
import torch
from collections import OrderedDict

# تعریف مدل PyTorch
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = torch.nn.Linear(2, 2)
        self.fc2 = torch.nn.Linear(2, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

# مدل اولیه
model = Net()

# تابع ذخیره‌سازی مدل
def save_model(model, path="global_model.pth"):
    torch.save(model.state_dict(), path)
    print(f"Model saved to {path}")

# استراتژی سفارشی‌شده با ذخیره مدل پس از هر Round
from flwr.common import parameters_to_ndarrays
from collections import OrderedDict

class SaveModelStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(self, rnd, results, failures):
        # اجرای عملیات تجمیع پیش‌فرض
        aggregated_weights = super().aggregate_fit(rnd, results, failures)

        # ذخیره مدل در صورت موفقیت‌آمیز بودن تجمیع
        if aggregated_weights is not None:
            print(f"Saving global model for round {rnd}...")

            # تبدیل Parameters به لیستی از وزن‌ها
            ndarrays = parameters_to_ndarrays(aggregated_weights[0])

            # بارگذاری وزن‌های جدید در مدل PyTorch
            state_dict = OrderedDict({
                f"layer_{i}": torch.tensor(weight) for i, weight in enumerate(ndarrays)
            })
            model.load_state_dict(state_dict, strict=False)

            # ذخیره مدل به‌روز شده
            save_model(model, path=f"global_model_round_{rnd}.pth")

        return aggregated_weights

# پیکربندی سرور
strategy = SaveModelStrategy()
config = fl.server.ServerConfig(num_rounds=1)  # تعداد دورها

# شروع سرور
print("Starting server...")
fl.server.start_server(
    server_address="127.0.0.1:8080",  # آدرس سرور
    strategy=strategy,               # استراتژی تجمیع
    config=config                    # پیکربندی سرور
)

# ذخیره مدل نهایی پس از پایان تمام دورها
save_model(model, path="final_global_model.pth")
print("Final model saved.")
