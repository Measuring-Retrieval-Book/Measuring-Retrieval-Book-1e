PDF=measuring-retrieval.pdf
HTML=measuring-retrieval.html

pdf:
	pandoc metadata.yaml chapters/*.md --css assets/book.css --toc --number-sections -o $(PDF)

html:
	pandoc metadata.yaml chapters/*.md --css assets/book.css --toc --number-sections -s -o $(HTML)

clean:
	rm -f $(PDF) $(HTML)
