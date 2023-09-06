.PHONY: executable

executable:
	chmod +x *.py
	chmod +x $(shell find ./models -name "*.py")
	chmod +x $(shell find ./tests -name "*.py")

pycodestyle:
	pycodestyle $(shell find ./models -name "*.py")
	pycodestyle $(shell find ./tests -name "*.py")