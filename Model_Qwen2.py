from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info

import torch
import pandas as pd
import time

model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct", 
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
min_pixels = 256*28*28
max_pixels = 1280*28*28
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct", min_pixels=min_pixels, max_pixels=max_pixels)

dataset = pd.read_csv('test.csv')

results = []
checkpoint_interval = 10
checkpoint_path = "test_output_4_2.csv"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}") 

batch_size = 1

try:
    results_df = pd.read_csv(checkpoint_path)
    start_index = len(results_df)
    results = results_df.to_dict(orient='records')
    print(f"Resuming from index {start_index}")
except FileNotFoundError:
    start_index = 0
    print(f"No checkpoint found. Starting from scratch.")

def process_batch(batch_rows):
    messages = []
    for row in batch_rows:
        image_link = row['image_link']
        entity_name = row['entity_name']
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image_link},
                    {"type": "text", "text": f"What is the {entity_name} in the image. Only write the answer in 2 words, value and its units"}
                ]
            }
        )
    texts = []
    for message in messages:
        text = processor.apply_chat_template([message], tokenize=False, add_generation_prompt=True)
        texts.append(text)

    image_inputs, video_inputs = process_vision_info(messages)

    assert len(texts) == len(image_inputs), "Mismatch between text and image inputs"

    inputs = processor(
        text=texts, 
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt"
    ).to(device)  

    with torch.no_grad():
        generated_ids = model.generate(**inputs, max_new_tokens=128)

    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_texts = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )

    batch_results = []
    for i, row in enumerate(batch_rows):
        batch_results.append({
            'image_link': row['image_link'],
            'entity_name': row['entity_name'],
            'description': output_texts[i]
        })

    return batch_results



for idx in range(start_index, len(dataset), batch_size):
    batch_rows = dataset.iloc[idx:idx+batch_size].to_dict(orient='records')

    start_time = time.time()
    
    try:
        batch_results = process_batch(batch_rows)
        results.extend(batch_results)
        end_time = time.time()
        batch_time = end_time - start_time
        print(f"Batch processed: {len(batch_rows)} images, Time taken: {batch_time:.2f} seconds")
        if (idx + len(batch_rows)) % checkpoint_interval == 0:
            pd.DataFrame(results).to_csv(checkpoint_path, index=False)
            print(f"Checkpoint saved at index {idx + len(batch_rows)}.")

    except torch.cuda.OutOfMemoryError:
        print(f"Out of Memory at batch starting index {idx}, skipping this batch.")
        torch.cuda.empty_cache()
        continue

    time.sleep(0.5)

output_df = pd.DataFrame(results)
output_df.to_csv('final_output_test_4_2.csv', index=False)
print("Processing completed. Final output saved.")

