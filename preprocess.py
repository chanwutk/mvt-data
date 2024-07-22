import argparse
import json
import pickle

import polars as pl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Path to input file as <input>." \
                        "The output prepreprocessed file will be saved as <input>.polar.pkl')
    args = parser.parse_args()

    print('Loading JSON', args.input, '...')
    with open(args.input, 'r') as f:
        data = json.load(f)

    datum = data[0]
    # datum['trajectory_id']
    # for d in data[:10]:
    #     print(d['direction'])

    # for k, v in datum.items():
    #     print(k, type(v))

    print('Mapping top-level types...')
    type_map = {}
    for datum in data:
        for k, v in datum.items():
            if k not in type_map:
                type_map[k] = set()
            type_map[k].add(type(v))


    print('Finding columns with mixed types...')
    mixed_type = []
    for k, v in type_map.items():
        if len(v) > 1:
            print('   ', v, k)
            mixed_type.append(k)


    print('Finding dtype of list types...')
    list_type = {}
    for datum in data:
        for k, v in datum.items():
            if isinstance(v, list):
                if k not in list_type:
                    list_type[k] = set()
                if not isinstance(v, list):
                    list_type[k].add(type(v))
                elif len(v) == 0:
                    list_type[k].add('empty')
                else:
                    if any(isinstance(vv, float) for vv in v):
                        list_type[k].add('float')
                    # if np.array(v).dtype == np.dtype('O'):
                    #     print(v)
                    elif any(isinstance(vv, int) for vv in v):
                        list_type[k].add('int')
                    else:
                        assert False, f"Containing unknown type: {v}"
                        # list_type[k].add('unknown')
                # if np.array(v).dtype == np.dtype('O'):
                #     print(v)

    for k, v in list_type.items():
        print('   ', k, v)


    # object_dtypes = []
    print('Finding float dtypes...')
    float_dtypes = []
    for k, v in list_type.items():
        # if len(v) > 1 and np.dtype('O') in v:
        #     # print(k, v)
        #     # object_dtypes.append(k)
        #     pass
        # el
        if 'float' in v:
            print('   ', k, v)
            float_dtypes.append(k)
        # elif len(v) == 1 and np.dtype('float64') in v:
        #     float_dtypes.append(k)


    print('Converting mixed types to float...')
    for datum in data:
        # aid = datum['upstream_av_id']
        # if (isinstance(aid, list) and any(isinstance(a, float) for a in aid)) or (aid is None):
        #     print(aid)
        for t in mixed_type:
            d = datum[t]
            if isinstance(d, list) or d is None:
                datum[t] = None
            else:
                datum[t] = float(d)
        for t in float_dtypes:
            d = datum[t]
            if d is None:
                continue
            if isinstance(d, float):
                d = [d]
            assert isinstance(d, list), type(d)
            datum[t] = [*map(lambda x: float(x) if x is not None else None, d)]
        # for t in object_dtypes:
        #     d = datum[t]
        #     datum[t] = [(None if dd is None else float(dd)) for dd in d]

    # data_dict = {}
    # for datum in data:
    #     for k in type_map:
    #         if k not in data_dict:
    #             data_dict[k] = []
    #         data_dict[k].append(datum[k])


    # for k, v in data_dict.items():
    #     try:
    #         pl.DataFrame({k: v})
    #     except TypeError as e:
    #         print(e)
    #         s = set()
    #         for vv in v:
    #             s.add(str(np.array(vv).dtype))
    #         print(s)
    #         print(k)
    #         print(np.array(v).shape)
    #         print([])
    #         break

    df = pl.from_records(data)

    print('Saving DataFrame...')
    with open(f'./{args.input}.pkl', 'wb') as f:
        pickle.dump(df, f)


if __name__ == '__main__':
    main()