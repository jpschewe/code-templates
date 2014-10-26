#ifndef SCHEWE_MACROS_HPP_
#define SCHEWE_MACROS_HPP_

#ifdef __GNUC__

	// check printfs
	#ifndef __APPLE__
		#define WARN_PRINTF(fmtstring, vararg) \
			__attribute__ ((format (printf, fmtstring, vararg)))
	#else
		#define WARN_PRINTF(fmtstring, vararg)
	#endif

	// warn if the return value isn't used..
	#define WARN_IF_UNUSED __attribute__ ((warn_unused_result))

	#define PACKED_STRUCT __attribute__((__packed__))

#ifdef __llvm__
    #define NO_OPTIMIZE_FUNCTION /* NOTHING - LLVM seems to do the right thing */
#else
    #define NO_OPTIMIZE_FUNCTION __attribute__((optimize("O0")))
#endif

#else

	#define WARN_PRINTF(fmtstring, vararg)
	#define WARN_IF_UNUSED

	#define PACKED_STRUCT NOT_IMPLEMENTED_ERROR

#endif



#endif /* SCHEWE_MACROS_HPP_ */
