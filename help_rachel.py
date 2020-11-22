import pdb
import numpy as np
import sys

fileName = "b0.5imputed.vcf"

#Function to read in the data
with open(fileName,"r",encoding = "latin-1") as f:
	totalData=[]
	for line in f.read().splitlines():
		if line[0] == "#":
			pass
		else:
			input_row = np.array(line.split("\t"))
			header = input_row[[0,2,1,3,4]]
			geno_vals = input_row[9:]
			final_vals = np.zeros((len(geno_vals), 3))
			for i in range(len(geno_vals)):
				single_geno = [geno_vals[i].split("|")[0]] +  geno_vals[i].split("|")[1].split(":")
				single_geno = [float(x) for x in single_geno]
				if (single_geno[0] == 1.0) & (single_geno[1] == 1.0):
					real_prob = single_geno[2]/2
					prob_homo_dom = (real_prob)**2
					prob_homo_rec = (1 - real_prob)**2
					prob_hetro = 1 - prob_homo_dom - prob_homo_rec
				else:
					real_prob = single_geno[2]
					prob_hetro = 1-abs(1-real_prob)
					prob_homo_rec = (1 - prob_hetro)**2
					prob_homo_dom = 1 - prob_homo_rec - prob_hetro

				final_vals[i,:] = (prob_homo_dom, prob_hetro, prob_homo_rec)

			if np.all(np.array([abs(x - 1) < 0.01 for x in np.sum(final_vals, axis=1)])):
				pass
			else:
				print("bad, : probs do not add to 1")
				pdb.set_trace()
				sys.exit()

			output_row = np.concatenate((header, final_vals.flatten()))
			totalData.append(output_row)

	totalData=np.array(totalData)
	np.savetxt("done_for_rachel.txt", totalData, "%s", '\t')
	pdb.set_trace()

print("eof")

