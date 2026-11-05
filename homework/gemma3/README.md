# Gemma 3 fine-tuning course summary

## Fine-tuning workflow

Supervised fine-tuning starts with a pretrained model and adapts it using examples of the desired behavior. The notebook loads the instruction-tuned Gemma 3 4B checkpoint with Unsloth, adds LoRA adapters, formats examples as conversations, trains with TRL's SFTTrainer, and saves the adapters and tokenizer for reuse.

## Gemma 3, LoRA, and PEFT

Gemma 3 4B supports image and text input. This exercise uses text and leaves the vision layers frozen. Loading the base weights in 4-bit precision reduces memory use.

Parameter-efficient fine-tuning (PEFT) updates a small part of a model. LoRA is a PEFT method that learns a low-rank weight update using two small matrices while keeping the original weight frozen. The supplied notebook uses rank 8, alpha 8, and dropout 0. It targets the language model's attention and MLP modules. The saved adapter needs the matching base checkpoint at inference time.

## Dataset preparation

The course CSV uses an input column for each Khmer prompt and an output column for the expected response. Format each pair as a user turn and an assistant turn with the Gemma 3 chat template. Response-only masking excludes prompt tokens from the loss. Before training, remove empty examples and keep repeated prompts in a single split to reduce leakage. Use a fixed seed for a reproducible train and validation split.

Databricks Dolly 15k provides a second instruction dataset. Its instruction and optional context form the user turn, and its response forms the assistant turn.

## Training configuration

| Setting | Supplied value | Effect |
| --- | --- | --- |
| Learning rate | 0.0002 | Controls the size of optimizer updates |
| Batch size per GPU | 2 | Controls how many examples are processed together |
| Gradient accumulation | 4 | Combines four batches before each update, for an effective batch of 8 on one GPU |
| Warm-up | 5 steps | Gradually increases the learning rate at the start |
| Maximum steps | 60 | Caps training at 60 optimizer updates |
| Scheduler | Linear | Reduces the learning rate after warm-up |

For a full pass over the training split, set the step limit to -1 and the epoch count to 1. Change one setting at a time when testing its effect.

## Training and validation loss

Training loss measures next-token prediction error on batches used to update the model. Validation loss measures that error on held-out examples. Falling losses on both splits suggest the model is learning patterns that transfer. Falling training loss alongside sustained rising validation loss suggests overfitting. Persistently high losses on both splits can indicate underfitting or a problem with the setup or data.

The supplied run logged training loss of **5.3791** at step 1, a minimum of **0.4490** at step 58, and **0.5751** at step 60. The model improved on its training batches. The run omitted validation, so its generalization is unknown.

For the dataset comparison, start both runs from the same base checkpoint with fresh adapters, keep the training settings fixed, and record validation loss every 10 steps. Compare the shape of the curves and the step with the lowest validation loss. Because the held-out sets contain different languages and tasks, compare generated answers on shared prompts to assess how each adapter behaves.

[Unsloth Gemma 3 guide](https://unsloth.ai/blog/gemma3) · [Hugging Face LoRA guide](https://huggingface.co/docs/peft/en/conceptual_guides/lora) · [TRL SFTTrainer](https://huggingface.co/docs/trl/main/en/sft_trainer) · [Databricks Dolly 15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k)
