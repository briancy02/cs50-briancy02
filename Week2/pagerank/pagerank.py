import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_all_pages = len(corpus.keys())
    model = dict()
    probability_random = (1 - damping_factor) / num_all_pages
    for key in corpus.keys():
      if len(corpus[page]) == 0:
        model[key] = 1 / num_all_pages
        continue
      model[key] = probability_random
      if key in corpus[page]:
        model[key] += damping_factor / len(corpus[page])
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    to_return = dict((el,0) for el in corpus.keys())
    cur_page = random.choice(list(corpus.keys()))
    for i in range(n):
      model = transition_model(corpus, cur_page, damping_factor)
      # Choose random page based on corpus weighting
      cur_page = random.choices(list(model.keys()), list(model.values()), k = 1)[0]
      to_return[cur_page] += 1
    for key in to_return.keys():
      to_return[key] /= n
    return to_return  


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # while error is > 0.01 continue iterating (loop through both dic n subtract)

    
    num_all_pages = len(corpus.keys())
    old_prs = dict((el, 1 / num_all_pages) for el in corpus.keys())
    new_prs = dict()
    is_good_enough = False
    while not is_good_enough:
      
      for key in corpus.keys():
        new_prs[key] = calc_pr(corpus, key, damping_factor, old_prs, num_all_pages)
      max_error = 0  
      for key in old_prs.keys():
        error = abs(old_prs[key] - new_prs[key])
        if error > max_error:
          max_error = error
      print(old_prs)
      print(new_prs)    
      if max_error < 0.0005:
        is_good_enough = True
      else:
        old_prs = new_prs  
        new_prs = dict()

    return new_prs    

def links(corpus, page):
  links_list = list()
  for key in corpus.keys():
    if page in corpus[key]:
      links_list.append(key)
  return links_list    

def calc_pr(corpus, page, damping_factor, old_prs, num_all_pages):
  if not links(corpus, page):
    return 1 / num_all_pages
  pr = (1 - damping_factor) / num_all_pages
  sum_value = 0
  for key in links(corpus, page):
    sum_value +=  old_prs[key] / len(links(corpus, key))
  pr += sum_value * damping_factor  
  return pr

if __name__ == "__main__":
    main()
