## Goal

The main objective of this project is to **determine the category of a financial transaction based on its description**.  

---

## Current Implementation

- Implemented using a **linear model: Logistic Regression**  
- Uses **TF-IDF vectorization** of transaction descriptions  
- Predicts categories such as `Grocery`, `Food & Drink`, `Services`, etc.  

### Sample Predictions

The following examples demonstrate the current behavior of the model:

```
Enter description: Bought iPhone.
['Grocery']
Enter description: Bought M1 MacBook Air.
['Grocery']
Enter description: Bought Coconut water.
['Grocery']
Enter description: Had coconut water.
['Food & Drink']
Enter description: Had banana.
['Food & Drink']
Enter description: Bought banana.
['Grocery']
Enter description: Had apple.
['Food & Drink']
Enter description: Bought Apple.
['Grocery']
Enter description: Bought pinapple.
['Grocery']
Enter description: Had pinapple.
['Food & Drink']
Enter description: Had hair cut
['Services']
Enter description: Cleaned bike.
['Services']
Enter description: Cleaned suit.
['Food & Drink']
Enter description: clean clothes.
['Food & Drink']
Enter description: bought clothes.
['Grocery']
```


> Note: While the model correctly identifies most transactions, there are some **misclassifications**, particularly for ambiguous items like `cleaned suit` or `clean clothes`.

---

## Future Plans

1. **Second Model:**  
   - Generate a **transaction description** automatically based on **category and amount**.  

2. **Automation Pipeline (iPhone):**  
   - When a UPI/credit card payment SMS is received, extract **amount, vendor, and other details** using regex.  
   - Pass the extracted details to the model to **predict category and generate description**.  
   - Automatically create a **ledger entry** in the Expenses app.  
   - Date and time are automatically handled by the app.  

3. **Current Workflow:**  
   - Using **Claude + Siri Shortcuts + Expenses app**, manually extract SMS details, pass to Claude with a prompt containing:
     - Fixed list of categories  
     - Sample written descriptions of past transactions  
   - Claude outputs **category and description**, which is then entered into the Expenses app.  
   - The entire process runs **automatically in the background** on iOS via Siri Shortcuts.  

---

## Friend Suggestions

- **Word2Vec:** Use embeddings to capture semantic similarity between words (e.g., “Had banana” vs “Bought banana”)  
- **Representative LLM:** Use a small fine-tuned language model to handle **complex description generation** and context-aware classification  