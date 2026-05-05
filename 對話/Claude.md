# Q-learning 與 SARSA 演算法比較實作

**Created:** 5/5/2026 14:42:35  
**Updated:** 5/5/2026 15:06:31  
**Exported:** 5/5/2026 15:08:07  
**Link:** [https://claude.ai/chat/b49fe37c-1d0c-45fd-a172-8e5009200c16](https://claude.ai/chat/b49fe37c-1d0c-45fd-a172-8e5009200c16)  

## Prompt:
2026/5/5 下午2:42:36

根據作業要求 給我一份完整可以繳交的檔案
"""
HW2: Q-learning 與 SARSA 演算法之比較研究

說明
一、作業目的
本作業旨在實作並比較兩種經典強化學習演算法——Q-learning 與 SARSA，透過相同環境與參數設定，分析其學習行為、收斂特性以及最終策略差異。
二、環境描述
本實驗採用經典的格子世界（Gridworld）問題，亦稱為「Cliff Walking」環境。環境設定如下：

* 使用一個矩形網格（例如 4 × 12）
* 起點（Start）位於左下角
* 終點（Goal）位於右下角
* 起點與終點之間的底部區域為「懸崖（Cliff）」
當代理（agent）進入懸崖時，會受到重大懲罰並回到起點。
三、問題設定

* 狀態空間（State Space）：所有網格位置
* 動作空間（Action Space）：上、下、左、右
* 獎勵機制（Reward）：
   * 每移動一步：−1
   * 掉入懸崖：−100，並回到起點
   * 到達終點：回合結束
* 策略（Policy）：ε-greedy（例如 ε = 0.1）
* 學習率（α）：例如 0.1
* 折扣因子（γ）：例如 0.9
* 訓練回合數（Episodes）：至少 500 回合
四、作業內容
（一）演算法實作
請分別實作以下兩種演算法：

* Q-learning（離策略方法，Off-policy）
* SARSA（同策略方法，On-policy）
兩者皆需建立並更新狀態-動作價值函數 Q(s, a)。
（二）訓練過程
在相同的環境與參數設定下，使用 ε-greedy 策略進行訓練，確保兩種方法的公平比較。
（三）結果分析
請針對以下面向進行比較與討論：

1. 學習表現
   * 繪製每一回合的累積獎勵（Total Reward）曲線
   * 比較收斂速度
2. 策略行為
   * 描述或視覺化最終學習到的路徑
   * 分析是否傾向冒險或保守
3. 穩定性分析
   * 比較學習過程中的波動程度
   * 討論探索（exploration）對結果的影響
五、理論比較與討論
在報告中，請說明以下概念：

* Q-learning 為離策略（Off-policy）方法，其更新基於「下一狀態的最佳可能行動」，即使該行動未實際執行。
* SARSA 為同策略（On-policy）方法，其更新基於「實際採取的行動」，因此會反映探索策略的影響。
一般而言：

* Q-learning 傾向學習到理論上的最優策略，但在訓練過程中可能較具風險。
* SARSA 則傾向學習在實際探索策略下較安全、穩定的行為。
六、結論要求
請總結兩種方法在本實驗中的差異，並說明：

* 哪一種方法收斂較快
* 哪一種方法較穩定
* 在何種情境下應選擇 Q-learning 或 SARSA

"""



## Response:
2026/5/5 下午2:46:20

````plaintext
View: Check available skills
````

Now I have the skill. Let me create a comprehensive report document.

````plaintext
Bash Tool: Setup npm docx and prepare Python simulation code
````

````plaintext
Bash Tool: Run Python simulation to generate learning curves data
````

````plaintext
Bash Tool: Generate learning curve chart
````

````plaintext
Bash Tool: Generate learning curve
````

````plaintext
Bash Tool: Generate chart with English labels
````

````plaintext
Bash Tool: Also generate a policy visualization chart
````

Now let me create the Word document report:

````plaintext
Create File: Create the HW2 report as a docx JS file
````

````plaintext
Bash Tool: Generate the Word document
````

````plaintext
Edit: Fix PageNumber usage
````

````plaintext
Edit: Fix footer page number
````

````plaintext
Bash Tool: Rebuild doc
````

````plaintext
Bash Tool: Validate the docx
````

````plaintext
Bash Tool: Copy to outputs
````

````plaintext
Present File: /mnt/user-data/outputs/HW2_Report.docx
````

報告已完成！以下是檔案內容摘要：

**📄 HW2_Report.docx** 包含完整六個章節：

1. **實驗目的** — 說明比較兩種演算法的核心動機
2. **環境描述** — Cliff Walking 環境設定、獎勵機制表格、完整實驗參數（ε=0.1, α=0.5, γ=0.9, 500回合）
3. **演算法實作** — Q-learning 與 SARSA 的完整 Python 程式碼、更新公式、對比表格
4. **實驗結果分析** — 含兩張圖表（學習曲線 + 策略視覺化），數據均來自真實模擬（50次執行平均），並有詳細數值分析
5. **理論分析** — Off-policy vs On-policy 本質差異、探索影響、Bellman 方程式對應
6. **結論** — 完整比較表格、方法選擇建議、總結

**模擬結果亮點：**
- Q-learning 後期均值：**-51.84**，波動標準差：11.46（較大）
- SARSA 後期均值：**-50.86**，波動標準差：9.76（較小、較穩定）
- 策略圖清楚呈現 Q-learning 靠崖冒險 vs SARSA 遠離懸崖的保守路線

> File: /mnt/user-data/outputs/HW2_Report.docx



## Prompt:
2026/5/5 下午2:55:28

我下載下來打不開



## Response:
2026/5/5 下午2:57:22

很抱歉！讓我改用另一種方式來建立文件。

````plaintext
Bash Tool: Check python-docx
````

````plaintext
Bash Tool: Build the docx using python-docx instead
````

````plaintext
Bash Tool: Copy to outputs
````

````plaintext
Present File: /mnt/user-data/outputs/HW2_Report.docx
````

這次改用 Python 的 `python-docx` 函式庫重新產生，格式更標準，應該可以直接用 Word 或 LibreOffice 開啟。

檔案內容完全保留，包含：
- 六大章節的完整內文
- 兩張實驗圖表（學習曲線 + 策略視覺化）
- 程式碼區塊、比較表格
- 參考資料

如果還是有問題，請告訴我你使用的是 Windows、Mac 還是手機，我可以改成 PDF 格式給你。

> File: /mnt/user-data/outputs/HW2_Report.docx


---
Powered by [Claude Exporter](https://www.ai-chat-exporter.net)