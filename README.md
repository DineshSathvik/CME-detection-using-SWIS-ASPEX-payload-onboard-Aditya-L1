# CME-detection-using-SWIS-ASPEX-payload-onboard-Aditya-L1

---

## **data/README.md**
```markdown
# CME Detection Data

This project does not include large `.cdf` data files.

To run the detection:
1. Visit https://pradan1.issdc.gov.in/al1/faq.xhtml
2. G to ASPEX_SWIS dataset to download the file.
3. Download `.cdf` files to the `data/` folder.
4. Run:
```bash
python src/detection.py data/your_file.cdf
