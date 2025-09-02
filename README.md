# Busy Buddy

Turn "busy work" into "buddy work" with Busy Buddy, an AI agent that helps answer coding questions by looking up relevant documentation. It uses the Context7 API under the hood to access high-quality code snippets and documentation. It provides examples, explanations, and is even transparent about its sources!

## Setup

This agent uses Gemini under the hood to run its AI agent. You'll need to make sure you have a `GEMINI_API_KEY` set in your environment. If it's not already set in your shell by default, it's recommended that you add a `.env` file with your Gemini API key like this:

```shell
GEMINI_API_KEY=<your_gemini_api_key>
```

After that, setting up [uv](https://docs.astral.sh/uv/) and a virtual environment can ensure that things run smoothly and easily. It's possible to run without it, but it's not recommended.

### `uv` Setup

#### Mac OS / Linux

Just run `make setup` to take care of installing `uv` (if needed) and generating the virtual environment needed for package isolation.

#### Windows

You can find [installation instructions for `uv`](https://docs.astral.sh/uv/getting-started/installation/) on their website.

After installing `uv`, you'll want to set up the virtual environment by running `uv sync --frozen`.

## How to run

### With `uv`

As long as `uv` is installed, you can just run this.

```shell
uv run python -m src.busy_buddy.main
```

This works on any OS with `uv`.

If you have Make installed, you can also just run `make run`.

### Without `uv` (not recommended)

If you'd prefer not to install `uv`, then you can just use pip to install the dependencies from `pyproject.toml`. You can also set up a virtual environment if you'd like to isolate the dependencies.

Then just run `./run.py`.

## Running Tests

You can use uv to run tests.

To do this, first, you'll want to run

```shell
uv sync --group dev
```

to ensure dev dependencies are installed.

Then you can just run

```shell
uv run pytest -q
```

## Examples

For each question heading below, Busy Buddy's clean markdown answer is shown along with the number of steps it had to take, the total time it took, and the input/output tokens that were used.

### How do I use re.split in Python?

```python
import re

# Example 1: Splitting a string by whitespace
text1 = "Hello world, how are you?"
result1 = re.split(r'\s+', text1)
print(f"Example 1 Result: {result1}")
# Expected Output: ['Hello', 'world,', 'how', 'are', 'you?']

# Example 2: Splitting a string by a comma or space, with a maximum of 2 splits
text2 = "apple, banana, cherry, date"
result2 = re.split(r'[, ]', text2, maxsplit=2)
print(f"Example 2 Result: {result2}")
# Expected Output: ['apple', '', 'banana', ' cherry, date'] (Note: empty string due to space after comma, and 
remaining string as last element)

# Example 3: Splitting and including the delimiters in the result
text3 = "one-two-three"
result3 = re.split(r'(-)', text3)
print(f"Example 3 Result: {result3}")
# Expected Output: ['one', '-', 'two', '-', 'three']
```

The `re.split()` function in Python's `re` module is used to split a string by occurrences of a regular expression pattern. It returns a list of strings.

- The first argument is the `pattern` (a regular expression) to split the string by.
- The second argument is the `string` to be split.
- An optional `maxsplit` argument can be provided to limit the number of splits. If `maxsplit` is non-zero, at most
`maxsplit` splits occur, and the remainder of the string is returned as the final element of the list.
- If capturing parentheses are used in the pattern, then the text of all matches of the group is also made part of the resulting list.

Sources: Internal knowledge.

> [Step 2: Duration 5.42 seconds| Input tokens: 7,166 | Output tokens: 506]

### How does Vue 3's watch function work?

The `watch` function in Vue 3 is used to react to changes in reactive data. It takes a source (which can be a ref, a reactive object, a getter function, or an array of multiple sources) and a callback function. The callback function is executed whenever the watched source changes, receiving the new value and the old value as arguments.

Here's a code example:

```javascript
import { ref, watch } from 'vue'

const count = ref(0)

watch(count, (newCount, prevCount) => {
  console.log(`Count changed from ${prevCount} to ${newCount}`)
})

// Example with immediate option to run the callback on initialization
const todoId = ref(1)
const data = ref(null)

watch(
  todoId,
  async () => {
    const response = await fetch(
      `https://jsonplaceholder.typicode.com/todos/${todoId.value}`
    )
    data.value = await response.json()
    console.log('Fetched data:', data.value)
  },
  { immediate: true }
)

count.value++ // This will trigger the first watcher
todoId.value++ // This will trigger the second watcher
```

**Explanation:**

- **Basic Usage**: `watch` can directly observe a `ref` (like `count` in the example). When `count.value` changes, the provided callback function will be invoked.
- **Callback Arguments**: The callback function receives two arguments: `newValue` (the current value of the watched source) and `oldValue` (the value before the change).
- **Options**: You can pass an optional options object as the third argument. Common options include:
  - `immediate: true`: The callback will be executed immediately when the watcher is created, and then again whenever the source changes.
  - `deep: true`: For watching reactive objects, this option enables deep traversal, meaning the callback will trigger even on nested mutations within the object.
  - `flush`: Controls the timing of the watcher callback execution.
- **Stopping a Watcher**: The `watch` function returns a function that, when called, stops the watcher from observing further changes.
- **Side Effect Cleanup**: The callback function can also receive an `onCleanup` argument, which is a function that registers a cleanup callback. This is useful for handling asynchronous operations to prevent memory leaks or stale requests.

**Sources:**
- https://github.com/vuejs/docs/blob/main/src/api/reactivity-core.md#_snippet_15
- https://github.com/vuejs/docs/blob/main/src/api/reactivity-core.md#_snippet_13
- https://github.com/vuejs/docs/blob/main/src/guide/essentials/watchers.md#_snippet_11
- https://github.com/vuejs/docs/blob/main/src/guide/essentials/watchers.md#_qa_4
- https://github.com/vuejs/docs/blob/main/src/api/reactivity-core.md#_snippet_19
- https://github.com/vuejs/docs/blob/main/src/api/reactivity-core.md#_snippet_22

> [Step 2: Duration 7.25 seconds| Input tokens: 17,670 | Output tokens: 808]

### Is there a Vuetify utility class to replace "padding: 8px"?

The Vuetify utility class to replace `padding: 8px` is `pa-2`.

**Code Example:**

```html
<div class="pa-2">This div has 8px padding on all sides.</div>
```

**Explanation:**
Vuetify provides a set of spacing helper classes to control margin and padding. The classes follow the pattern `{property}{direction}-{size}`. For padding, the property is `p`. To apply padding to all sides, the direction is `a`. The size `2` corresponds to `8px`.

**Sources:**
* https://github.com/vuetifyjs/vuetify/blob/master/packages/docs/src/pages/en/styles/spacing.md#_snippet_20
* https://github.com/vuetifyjs/vuetify/blob/master/packages/docs/src/pages/en/styles/spacing.md#_snippet_12

> [Step 2: Duration 3.26 seconds| Input tokens: 18,207 | Output tokens: 260]
