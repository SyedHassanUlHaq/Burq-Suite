// NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE
// This is an automatically generated file by mahnoor on و 01:04:11 PKT ت 21 نومبر 2022
//
// cmd:    swerv -target=default -set build_axi4 
//
`define RV_ROOT "/home/mahnoor/burqnew/cores/swerv"
`define RV_PIC_MEIGWCTRL_MASK 'h3
`define RV_PIC_TOTAL_INT_PLUS1 32
`define RV_PIC_MPICCFG_OFFSET 'h3000
`define RV_PIC_MEIGWCLR_MASK 'h0
`define RV_PIC_MEIGWCLR_COUNT 31
`define RV_PIC_OFFSET 10'hc0000
`define RV_PIC_MEIPL_MASK 'hf
`define RV_PIC_MEIE_MASK 'h1
`define RV_PIC_BASE_ADDR 32'hf00c0000
`define RV_PIC_MEIGWCTRL_OFFSET 'h4000
`define RV_PIC_MEIP_MASK 'h0
`define RV_PIC_MEIPL_OFFSET 'h0000
`define RV_PIC_REGION 4'hf
`define RV_PIC_MEIPT_COUNT 31
`define RV_PIC_BITS 15
`define RV_PIC_MEIE_OFFSET 'h2000
`define RV_PIC_MEIE_COUNT 31
`define RV_PIC_MEIPT_OFFSET 'h3004
`define RV_PIC_MEIGWCTRL_COUNT 31
`define RV_PIC_INT_WORDS 1
`define RV_PIC_MEIPL_COUNT 31
`define RV_PIC_MEIP_OFFSET 'h1000
`define RV_PIC_MEIP_COUNT 1
`define RV_PIC_SIZE 32
`define RV_PIC_MEIPT_MASK 'h0
`define RV_PIC_MPICCFG_COUNT 1
`define RV_PIC_TOTAL_INT 31
`define RV_PIC_MEIGWCLR_OFFSET 'h5000
`define RV_PIC_MPICCFG_MASK 'h1
`define RV_IFU_BUS_PRTY 2
`define RV_LSU_BUS_ID 1
`define RV_DMA_BUS_ID 1
`define RV_SB_BUS_TAG 1
`define RV_BUS_PRTY_DEFAULT 2'h3
`define RV_SB_BUS_ID 1
`define RV_SB_BUS_PRTY 2
`define RV_DMA_BUS_TAG 1
`define RV_LSU_BUS_TAG 3
`define RV_LSU_BUS_PRTY 2
`define RV_IFU_BUS_ID 1
`define RV_DMA_BUS_PRTY 2
`define RV_IFU_BUS_TAG 3
`define RV_LSU_NUM_NBLOAD 4
`define RV_ICCM_ICACHE 1
`define RV_BITMANIP_ZBF 0
`define RV_DIV_NEW 1
`define RV_BITMANIP_ZBR 0
`define RV_FAST_INTERRUPT_REDIRECT 1
`define RV_LSU_NUM_NBLOAD_WIDTH 2
`define RV_BITMANIP_ZBP 0
`define RV_FPGA_OPTIMIZE 1
`define RV_LSU2DMA 0
`define RV_DMA_BUF_DEPTH 5
`define RV_BITMANIP_ZBS 1
`define RV_BITMANIP_ZBB 1
`define RV_BITMANIP_ZBE 0
`define RV_LSU_STBUF_DEPTH 4
`define RV_TIMER_LEGAL_EN 1
`define RV_DIV_BIT 4
`define RV_BITMANIP_ZBC 1
`define RV_BITMANIP_ZBA 1
`define RV_BHT_GHR_HASH_1 
`define RV_BHT_ADDR_LO 2
`define RV_BHT_ARRAY_DEPTH 256
`define RV_BHT_ADDR_HI 9
`define RV_BHT_GHR_RANGE 7:0
`define RV_BHT_HASH_STRING {hashin[8+1:2]^ghr[8-1:0]}// cf2
`define RV_BHT_GHR_SIZE 8
`define RV_BHT_SIZE 512
`define REGWIDTH 32
`define RV_ICCM_BITS 16
`define RV_ICCM_OFFSET 10'he000000
`define RV_ICCM_INDEX_BITS 12
`define RV_ICCM_SADR 32'hee000000
`define RV_ICCM_NUM_BANKS_4 
`define RV_ICCM_SIZE_64 
`define RV_ICCM_BANK_INDEX_LO 4
`define RV_ICCM_RESERVED 'h1000
`define RV_ICCM_ROWS 4096
`define RV_ICCM_BANK_BITS 2
`define RV_ICCM_DATA_CELL ram_4096x39
`define RV_ICCM_SIZE 64
`define RV_ICCM_EADR 32'hee00ffff
`define RV_ICCM_NUM_BANKS 4
`define RV_ICCM_REGION 4'he
`define RV_ICCM_BANK_HI 3
`define RV_ICCM_ENABLE 1
`define RV_INST_ACCESS_ADDR5 'h00000000
`define RV_DATA_ACCESS_MASK6 'hffffffff
`define RV_INST_ACCESS_ENABLE5 1'h0
`define RV_INST_ACCESS_ENABLE2 1'h0
`define RV_INST_ACCESS_ENABLE6 1'h0
`define RV_DATA_ACCESS_ENABLE3 1'h0
`define RV_INST_ACCESS_ADDR1 'h00000000
`define RV_DATA_ACCESS_ADDR2 'h00000000
`define RV_DATA_ACCESS_MASK4 'hffffffff
`define RV_INST_ACCESS_ENABLE1 1'h0
`define RV_INST_ACCESS_MASK1 'hffffffff
`define RV_DATA_ACCESS_ADDR4 'h00000000
`define RV_DATA_ACCESS_MASK2 'hffffffff
`define RV_DATA_ACCESS_ADDR6 'h00000000
`define RV_INST_ACCESS_MASK5 'hffffffff
`define RV_DATA_ACCESS_ENABLE6 1'h0
`define RV_DATA_ACCESS_ENABLE2 1'h0
`define RV_DATA_ACCESS_ENABLE5 1'h0
`define RV_DATA_ACCESS_ADDR5 'h00000000
`define RV_INST_ACCESS_MASK6 'hffffffff
`define RV_INST_ACCESS_ADDR2 'h00000000
`define RV_INST_ACCESS_MASK4 'hffffffff
`define RV_DATA_ACCESS_ADDR1 'h00000000
`define RV_INST_ACCESS_ENABLE3 1'h0
`define RV_INST_ACCESS_MASK2 'hffffffff
`define RV_INST_ACCESS_ADDR4 'h00000000
`define RV_DATA_ACCESS_MASK1 'hffffffff
`define RV_DATA_ACCESS_ENABLE1 1'h0
`define RV_DATA_ACCESS_MASK5 'hffffffff
`define RV_INST_ACCESS_ADDR6 'h00000000
`define RV_INST_ACCESS_MASK3 'hffffffff
`define RV_INST_ACCESS_ADDR0 'h00000000
`define RV_DATA_ACCESS_ENABLE7 1'h0
`define RV_INST_ACCESS_ADDR7 'h00000000
`define RV_DATA_ACCESS_ENABLE4 1'h0
`define RV_INST_ACCESS_MASK7 'hffffffff
`define RV_INST_ACCESS_ENABLE0 1'h0
`define RV_INST_ACCESS_MASK0 'hffffffff
`define RV_INST_ACCESS_ADDR3 'h00000000
`define RV_DATA_ACCESS_ADDR0 'h00000000
`define RV_INST_ACCESS_ENABLE7 1'h0
`define RV_DATA_ACCESS_MASK3 'hffffffff
`define RV_INST_ACCESS_ENABLE4 1'h0
`define RV_DATA_ACCESS_ADDR7 'h00000000
`define RV_DATA_ACCESS_MASK7 'hffffffff
`define RV_DATA_ACCESS_ADDR3 'h00000000
`define RV_DATA_ACCESS_MASK0 'hffffffff
`define RV_DATA_ACCESS_ENABLE0 1'h0
`define RV_RESET_VEC 'h80000000
`define RV_TARGET default
`define RV_DCCM_ROWS 4096
`define RV_DCCM_RESERVED 'h1400
`define RV_LSU_SB_BITS 16
`define RV_DCCM_INDEX_BITS 12
`define RV_DCCM_SADR 32'hf0040000
`define RV_DCCM_BITS 16
`define RV_DCCM_OFFSET 28'h40000
`define RV_DCCM_NUM_BANKS_4 
`define RV_DCCM_WIDTH_BITS 2
`define RV_DCCM_SIZE_64 
`define RV_DCCM_REGION 4'hf
`define RV_DCCM_BYTE_WIDTH 4
`define RV_DCCM_ENABLE 1
`define RV_DCCM_ECC_WIDTH 7
`define RV_DCCM_EADR 32'hf004ffff
`define RV_DCCM_BANK_BITS 2
`define RV_DCCM_DATA_CELL ram_4096x39
`define RV_DCCM_SIZE 64
`define RV_DCCM_DATA_WIDTH 32
`define RV_DCCM_FDATA_WIDTH 39
`define RV_DCCM_NUM_BANKS 4
`define RV_CONFIG_KEY 32'hdeadbeef
`define RV_ICACHE_BANKS_WAY 2
`define RV_ICACHE_TAG_LO 13
`define RV_ICACHE_BEAT_ADDR_HI 5
`define RV_ICACHE_DATA_CELL ram_512x71
`define RV_ICACHE_TAG_BYPASS_ENABLE 1
`define RV_ICACHE_ENABLE 1
`define RV_ICACHE_TAG_CELL ram_128x25
`define RV_ICACHE_WAYPACK 1
`define RV_ICACHE_TAG_NUM_BYPASS 2
`define RV_ICACHE_ECC 1
`define RV_ICACHE_BANK_LO 3
`define RV_ICACHE_NUM_LINES_BANK 64
`define RV_ICACHE_BYPASS_ENABLE 1
`define RV_ICACHE_BANK_WIDTH 8
`define RV_ICACHE_NUM_LINES 256
`define RV_ICACHE_LN_SZ 64
`define RV_ICACHE_TAG_NUM_BYPASS_WIDTH 2
`define RV_ICACHE_TAG_DEPTH 128
`define RV_ICACHE_NUM_WAYS 2
`define RV_ICACHE_NUM_BEATS 8
`define RV_ICACHE_BANK_BITS 1
`define RV_ICACHE_SIZE 16
`define RV_ICACHE_DATA_INDEX_LO 4
`define RV_ICACHE_BEAT_BITS 3
`define RV_ICACHE_FDATA_WIDTH 71
`define RV_ICACHE_NUM_BYPASS_WIDTH 2
`define RV_ICACHE_NUM_LINES_WAY 128
`define RV_ICACHE_NUM_BYPASS 2
`define RV_ICACHE_INDEX_HI 12
`define RV_ICACHE_BANK_HI 3
`define RV_ICACHE_SCND_LAST 6
`define RV_ICACHE_DATA_WIDTH 64
`define RV_ICACHE_2BANKS 1
`define RV_ICACHE_DATA_DEPTH 512
`define RV_ICACHE_STATUS_BITS 1
`define RV_ICACHE_TAG_INDEX_LO 6
`define RV_RET_STACK_SIZE 8
`define RV_XLEN 32
`define RV_NMI_VEC 'h11110000
`define RV_UNUSED_REGION3 'h50000000
`define RV_EXTERNAL_DATA_1 'hb0000000
`define RV_UNUSED_REGION6 'h20000000
`define RV_SERIALIO 'hd0580000
`define RV_UNUSED_REGION8 'h00000000
`define RV_UNUSED_REGION5 'h30000000
`define RV_UNUSED_REGION4 'h40000000
`define RV_EXTERNAL_DATA 'hc0580000
`define RV_UNUSED_REGION2 'h60000000
`define RV_UNUSED_REGION7 'h10000000
`define RV_DEBUG_SB_MEM 'ha0580000
`define RV_UNUSED_REGION1 'h70000000
`define RV_UNUSED_REGION0 'h90000000
`define TEC_RV_ICG clockhdr
`define RV_TOP `TOP.rvtop
`define SDVT_AHB 0
`define RV_STERR_ROLLBACK 0
`define RV_ASSERT_ON 
`define RV_BUILD_AXI_NATIVE 1
`define RV_BUILD_AXI4 1
`define RV_EXT_DATAWIDTH 64
`define CPU_TOP `RV_TOP.swerv
`define CLOCK_PERIOD 100
`define TOP tb_top
`define RV_LDERR_ROLLBACK 1
`define RV_EXT_ADDRWIDTH 32
`define RV_NUMIREGS 32
`define RV_BTB_ADDR_HI 9
`define RV_BTB_ENABLE 1
`define RV_BTB_SIZE 512
`define RV_BTB_BTAG_SIZE 5
`define RV_BTB_INDEX1_LO 2
`define RV_BTB_INDEX3_LO 18
`define RV_BTB_INDEX2_HI 17
`define RV_BTB_FOLD2_INDEX_HASH 0
`define RV_BTB_ADDR_LO 2
`define RV_BTB_INDEX1_HI 9
`define RV_BTB_INDEX3_HI 25
`define RV_BTB_INDEX2_LO 10
`define RV_BTB_TOFFSET_SIZE 12
`define RV_BTB_BTAG_FOLD 0
`define RV_BTB_ARRAY_DEPTH 256
`undef RV_ASSERT_ON
