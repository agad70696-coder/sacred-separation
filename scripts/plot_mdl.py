import matplotlib.pyplot as plt
models = ['M6','M7','M8','M9','M10','M11']
total_85 = [1639,1638,1638,1634,92,2025]
total_full = [118484,118484,118484,118484,117593,2025]
fig, ax = plt.subplots(1,2, figsize=(10,4))
ax[0].bar(models, total_85)
ax[0].set_title('85 Ayat - WINNER M10=92 bits')
ax[0].set_ylabel('TOTAL bits')
ax[1].bar(models, total_full)
ax[1].set_title('6236 Ayat FULL - WINNER M11=2025 bits')
ax[1].set_ylabel('TOTAL bits')
plt.tight_layout()
plt.savefig('figures/mdl_winners.png', dpi=200)
print("saved figures/mdl_winners.png")
