
#with open('pickles/SUNO/Sept_16_Suno_Diagonal_new8_Beat_Comp.pkl', 'rb') as loadfile:
    #comp_list = pickle.load(loadfile)

    x = 0
    count = 0
    sum_corr = 0
    mx = len(comp_list)
    same_counter = 0
    print('')
    filtered = []
    while x < mx:
        cp = comp_list[x]
        if cp.y_promptID == cp.x_promptID:
            if cp.y_studentID == cp.x_studentID:
                same_counter = same_counter + 1
            else:
                if cp.y_studentID != cp.x_studentID:
                    filtered.append(cp)
        sum_corr = sum_corr + cp.d_corr
        x = x + 1
    print(f' There are {same_counter} Comparisons in same prompt within the same student.')
    print('')
    print(f' Total No. Comparisons = {len(comp_list)}')
    print(f' *******   Length of filtered list = {len(filtered)}')
    print('')
    print(f'-- Avg. Correlation For All Comparisons: {sum_corr / len(comp_list)}')
    x = 0
    extract_list = []
    while x < 8:
        p_num = x + 1
        pairs = []
        in_prompt = []
        p_finder = 0
        while p_finder < len(filtered):
            p1 = filtered[p_finder].y_promptID
            p2 = filtered[p_finder].x_promptID
            if p1 == x and p2 == x:
                in_prompt.append(filtered[p_finder])
            p_finder = p_finder + 1
        ctr1 = 0
        above_threshold = []
        in_threshold_range = []
        while ctr1 < len(in_prompt):
            cp2 = in_prompt[ctr1]
            if cp2.d_corr >= correlation_min:
                above_threshold.append(cp2)
            # if .707 <= cp2.d_corr <= .727:
            if .740 <= cp2.d_corr <= .860:
                in_threshold_range.append(cp2.d_corr)
            ctr1 = ctr1 + 1
        print(f'----- FOR PROMPT {p_num} ----- ')
        print(' ')
        print(f'Total no. of Comparisons in prompt {p_num} w/ Diff Students = {len(in_prompt)}')
        print(' ')
        min_corr = min(in_prompt, key=lambda compare: compare.d_corr)
        print(f'.......  Lowest Correlation in Comparisons w/ Diff Students= {round(min_corr.d_corr, 4)}')
        print(' ')
        avg_corr = sum(c.d_corr for c in in_prompt) / len(in_prompt)
        print(f'.......  Avg. Correlation in Comparisons w/ Diff Students: '
              f'{round(avg_corr, 4)}')
        print(' ')
        print(f'Total no. of Comparisons  w/ Diff Students >= Sim Correlation: {len(above_threshold)}')
        print(' ')
        print(f'.......  % of Comparisons >= Sim Correlation: {round((len(above_threshold)/len(in_prompt)), 4)}')
        print(' ')
        min_above = min(above_threshold, key=lambda thresh: thresh.d_corr)
        print(f'.......  Min Corr >= Sim Correlation: {round(min_above.d_corr, 4)}')
        print(' ')
        max_above = max(above_threshold, key=lambda thresh: thresh.d_corr)
        print(f'.......  Max Corr >= Sim Correlation: {round(max_above.d_corr, 4)}')
        print(' ')
        print(f'Total no. of Correlations in Comparisons w/ Diff Students btw .707 & .727: {len(in_threshold_range)}')
        print(' ')
        percent_range = len(in_threshold_range) / len(in_prompt)
        print(f'........  % of Comparisons btw .707 & .727: {round(percent_range, 4)}')
        print(' ')
        min_cmp = min(above_threshold, key=lambda min_c: min_c.d_corr)
        print(f'      -- Min Correlation above Threshold: {round(min_cmp.d_corr, 4)}  ')
        for compare1 in above_threshold:
            if compare1.offset > 0:
                break
        min_cmp = compare1
        pairs.append(min_cmp)
        std_y = min_cmp.y_studentID + 1
        sng_y = min_cmp.y_songID + 1
        std_x = min_cmp.x_studentID + 1
        sng_x = min_cmp.x_songID + 1
        print(f'        *** lower comparison example prompt: {p_num} ***')
        print(f'                :: Student Y {std_y}')
        print(f'                :: Song Y {sng_y}')
        print(f'                :: Student X {std_x}')
        print(f'                :: Song X {sng_x}')
        print(' ')
        max_cmp = max(above_threshold, key=lambda max_c: max_c.d_corr)
        print(f'      -- Max Correlation above Threshold: {round(max_cmp.d_corr, 4)}  ')
        for compare2 in reversed(above_threshold):
            if compare2.offset > 0:
                break
        max_cmp = compare2
        pairs.append(max_cmp)
        std_y = max_cmp.y_studentID + 1
        sng_y = max_cmp.y_songID + 1
        std_x = max_cmp.x_studentID + 1
        sng_x = max_cmp.x_songID + 1
        print(f'        *** higher comparison example prompt: {p_num} ***')
        print(f'                :: Student Y {std_y}')
        print(f'                :: Song Y {sng_y}')
        print(f'                :: Student X {std_x}')
        print(f'                :: Song X {sng_x}')
        print(' ')
        if len(pairs) == 2:
            print(f'found 2 max/min comparisons in this prompt: {p_num}')
        else:
            print(f'did not find 2 max/min comparisons in this prompt: {p_num}')
        extract_list.append(pairs)
        print(f'{p_num} & {len(in_prompt)} & {round(min_corr.d_corr, 4)} & {round(avg_corr, 4)} & '
              f'\\ {round(max_above.d_corr, 4)} \\\\')
        print( '')
        print(f'{p_num} & {len(in_prompt)} & {round((len(above_threshold)/len(in_prompt)) , 4)}% & '
              f'\\  {round(percent_range, 4)}% \\\\')
        x = x + 1
    ctr2 = 0
    while ctr2 < len(extract_list):
        p_num = ctr2 + 1
        current_comp = extract_list[ctr2]
        min_cmp = current_comp[0]
        max_cmp = current_comp[1]
        if min_cmp.y_promptID == max_cmp.x_promptID:
            diagonal_list = common_get_prompt_list(min_cmp.y_promptID, to_load_pickle_date)
        else:
            print(f' Oops...these 2 comparisons not from same prompt: {p_num}')
        print(f' Getting Heatmaps and Audio for 2 Comparisons from Prompt {p_num}')
        title_prefix1 = p_num + .1
        title_prefix2 = p_num + .8
        get_songs(diagonal_list, min_cmp, title_prefix1)
        get_songs(diagonal_list, max_cmp, title_prefix2)
        ctr2 = ctr2 + 1
